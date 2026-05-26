"""
procesador_pedidos.py — Orquestador principal de compras.

Implementa el flujo de compras de acuerdo a las 4 Reglas de Negocio Consolidadas:
1. Validación de Pedido y Disponibilidad
2. Cálculo de Descuentos
3. Impuestos y Cargos
4. Seguridad de Pago y Auditoría Persistente
"""

import os
import time
import json
import logging

from database_mock import (
    obtener_producto_por_id,
    obtener_usuario_por_id,
    actualizar_stock,
    HISTORIAL,
)
from logic.calculadora_impuestos import (
    calcular_iva_complejo,
    calcular_iva_electronico,
    calcular_descuento_fidelidad,
    obtener_porcentaje_descuento_monto,
)
from logic.validador_negocio import (
    validar_transaccion_segura,
    validar_y_aplicar_cupon,
    verificar_limite_diario,
    registrar_gasto_diario,
    validar_categoria_permitida,
)
from utils.formatter import determinar_prioridad, aplicar_tarifa_internacional

CANTIDAD_MAXIMA = 50


def procesar_compra(id_usuario: int, id_producto: int, cantidad: int,
                    codigo_cupon: str | None = None) -> dict:
    """
    Orquestador de compra que aplica secuencialmente las 4 Reglas de Negocio Consolidadas.
    """
    usuario = obtener_usuario_por_id(id_usuario)
    producto = obtener_producto_por_id(id_producto)

    if not producto or not usuario:
        return {"error": "Datos no encontrados"}

    # ---------------------------------------------------------------------------
    # REGLA 1: VALIDACIÓN DE PEDIDO Y DISPONIBILIDAD
    # ---------------------------------------------------------------------------
    if cantidad <= 0:
        return {"error": "Cantidad inválida"}

    if cantidad > CANTIDAD_MAXIMA:
        return {"error": "Cantidad máxima excedida"}

    if producto["stock"] < cantidad:
        return {"error": "No hay stock suficiente"}

    if not validar_categoria_permitida(producto["categoria"], usuario["vip"]):
        return {"error": "Categoría no permitida para este tipo de usuario"}

    # ---------------------------------------------------------------------------
    # REGLA 2: CÁLCULO DE DESCUENTOS
    # ---------------------------------------------------------------------------
    subtotal = producto["precio"] * cantidad

    # Descuento por monto (no acumulativo, 5% si > $50, 10% si > $200)
    descuento_monto = obtener_porcentaje_descuento_monto(subtotal)
    
    # Descuento VIP (+10% adicional acumulativo)
    descuento_vip = 0.10 if usuario.get("vip") else 0.0
    
    descuento_base_total = descuento_monto + descuento_vip
    total_con_descuento = subtotal * (1 - descuento_base_total)

    # Descuento por fidelidad (3% adicional si > 10 compras previas)
    desc_fidelidad = calcular_descuento_fidelidad(usuario)
    if desc_fidelidad:
        total_con_descuento *= (1 - desc_fidelidad)

    # ---------------------------------------------------------------------------
    # REGLA 3: CÁLCULO DE IMPUESTOS Y CARGOS
    # ---------------------------------------------------------------------------
    # IVA: 10% estándar, 9% reducido para electrónicos
    if producto["categoria"] == "electronico":
        iva = calcular_iva_electronico(total_con_descuento, es_vip=usuario["vip"])
    else:
        iva = calcular_iva_complejo(total_con_descuento, es_vip=usuario["vip"])

    total_con_iva = total_con_descuento + iva

    # Validación y aplicación del cupón (Regla 2, puede lanzar error si es inactivo/usado)
    try:
        total_con_iva, descuento_cupon = validar_y_aplicar_cupon(total_con_iva, codigo_cupon, id_usuario)
    except ValueError as e:
        return {"error": str(e)}

    # Recargo internacional (2% si país es "US")
    total_final = aplicar_tarifa_internacional(total_con_iva, usuario["pais"])

    # ---------------------------------------------------------------------------
    # REGLA 4: SEGURIDAD DE PAGO Y AUDITORÍA PERSISTENTE
    # ---------------------------------------------------------------------------
    # Validación de saldo disponible
    es_valido_saldo, motivo_saldo = validar_transaccion_segura(usuario, total_final)
    if not es_valido_saldo:
        return {"error": motivo_saldo}

    # Validación de límite de gasto diario ($3,000)
    if not verificar_limite_diario(id_usuario, total_final):
        return {"error": "Límite de gasto diario alcanzado"}

    # Ejecución de transacciones y actualizaciones
    usuario["saldo"] -= total_final
    actualizar_stock(id_producto, cantidad)
    registrar_gasto_diario(id_usuario, total_final)

    # Prioridad de envío (> $400 es ALTA, de lo contrario NORMAL)
    prioridad = determinar_prioridad(total_final)

    # Registro de transacciones
    log_entry = {
        "id_usuario": id_usuario,
        "id_producto": id_producto,
        "cantidad": cantidad,
        "total": total_final,
        "prioridad": prioridad,
        "codigo_cupon": codigo_cupon,
        "timestamp": int(time.time()),
    }
    
    # Registro en memoria
    HISTORIAL.append(log_entry)

    # Registro en archivo de log persistente
    try:
        log_dir = os.path.dirname(os.path.abspath(__file__))
        log_path = os.path.join(log_dir, "system_audit.log")
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")
    except Exception as e:
        logging.error(f"Error al escribir en el log persistente: {e}")

    return {
        "status": "success",
        "total": total_final,
        "iva": iva,
        "descuento_applied": descuento_base_total,  # Para mantener compatibilidad con tests
        "descuento_aplicado": descuento_base_total,
        "descuento_fidelidad": desc_fidelidad,
        "descuento_cupon": descuento_cupon,
        "prioridad": prioridad,
    }
