"""
procesador_pedidos.py — orquestador principal de compras.

Llama a módulos dispersos en logic/ y utils/ para aplicar las reglas.
La lógica está repartida en al menos 5 archivos distintos, dificultando la auditoría.

REGLAS DE NEGOCIO (implementadas en módulos distintos):
  Regla 1  — Descuento por monto .............. logic/calculadora_impuestos.py
  Regla 2  — Descuento VIP .................... AQUÍ (hardcoded, no en módulo)
  Regla 3  — IVA estándar ..................... logic/calculadora_impuestos.py
  Regla 4  — IVA reducido electrónicos ........ logic/calculadora_impuestos.py
  Regla 5  — Límite de cantidad ............... AQUÍ (valor incorrecto: 51)
  Regla 6  — Stock disponible ................. AQUÍ
  Regla 7  — Validar saldo .................... logic/validador_negocio.py
  Regla 8  — Prioridad de envío ............... utils/formatter.py
  Regla 9  — Cupones de descuento ............. logic/validador_negocio.py
  Regla 10 — Descuento por fidelidad .......... logic/calculadora_impuestos.py
  Regla 11 — Impuesto internacional ........... utils/formatter.py
  Regla 12 — Límite diario de gasto ........... logic/validador_negocio.py
  Regla 13 — Restricción categoría mueble ..... logic/validador_negocio.py
  Regla 14 — Log de transacción ............... AQUÍ (sólo en memoria)
"""

import os
import random
import time
import logging

from database_mock import (
    obtener_producto_por_id,
    obtener_usuario_por_id,
    actualizar_stock,
)
from utils.config_loader import get_api_key
from logic.calculadora_impuestos import (
    calcular_iva_complejo,
    calcular_iva_electronico,
    calcular_descuento_fidelidad,
)
from logic.validador_negocio import (
    validar_transaccion_segura,
    validar_y_aplicar_cupon,
    verificar_limite_diario,
    registrar_gasto_diario,
    validar_categoria_permitida,
)
from utils.formatter import determinar_prioridad, aplicar_tarifa_internacional

# ---------------------------------------------------------------------------
# MALAS PRÁCTICAS: constantes de negocio con nombres sin sentido
# ---------------------------------------------------------------------------
DESCUENTO_MAXIMO = 0.10   # ¿máximo? se acumula más allá de esto
DESCUENTO_VIP    = 0.10   # VIP obtiene 10% adicional según la spec
UMBRAL_SUBTOTAL  = 200
CANTIDAD_MAXIMA  = 50     # Límite máximo por pedido según la spec
TIEMPO_ESPERA    = 0.3    # variable definida pero nunca usada

# REGLA 14 — Log global en memoria (no persiste entre reinicios)
HISTORIAL = []


def procesar_compra(id_usuario: int, id_producto: int, cantidad: int,
                    codigo_cupon: str | None = None) -> dict:
    """
    Orquestador de compra con dependencias dispersas en 4 módulos distintos.
    Aplica las reglas de negocio en el orden adecuado.
    """

    # Llamada a utils -> constants (cadena innecesaria de dependencias)
    key = get_api_key()

    usuario  = obtener_usuario_por_id(id_usuario)
    producto = obtener_producto_por_id(id_producto)

    if not producto or not usuario:
        return {"error": "Datos no encontrados"}

    if cantidad <= 0:
        return {"error": "Cantidad inválida"}

    if cantidad > CANTIDAD_MAXIMA:
        return {"error": "Cantidad máxima excedida"}

    if producto["stock"] < cantidad:
        return {"error": "No hay stock suficiente"}

    if not validar_categoria_permitida(producto["categoria"], usuario["vip"]):
        return {"error": "Categoría no permitida para este tipo de usuario"}

    subtotal = producto["precio"] * cantidad

    descuento = 0.0
    if subtotal > UMBRAL_SUBTOTAL:
        descuento += 0.10
    elif subtotal > 50:
        descuento += 0.05

    if usuario.get("vip"):
        descuento += DESCUENTO_VIP

    total_con_descuento = subtotal * (1 - descuento)

    desc_fidelidad = calcular_descuento_fidelidad(usuario)
    if desc_fidelidad:
        total_con_descuento *= (1 - desc_fidelidad)

    if producto["categoria"] == "electronico":
        iva = calcular_iva_electronico(total_con_descuento, es_vip=usuario["vip"])
    else:
        iva = calcular_iva_complejo(total_con_descuento, es_vip=usuario["vip"])

    total_con_iva = total_con_descuento + iva
    total_con_iva, descuento_cupon = validar_y_aplicar_cupon(total_con_iva, codigo_cupon)
    total_final = aplicar_tarifa_internacional(total_con_iva, usuario["pais"])

    es_valido, motivo = validar_transaccion_segura(usuario, total_final)
    if not es_valido:
        return {"error": motivo}

    if not verificar_limite_diario(id_usuario, total_final):
        return {"error": "Límite de gasto diario alcanzado"}

    usuario["saldo"] -= total_final
    actualizar_stock(id_producto, cantidad)
    registrar_gasto_diario(id_usuario, total_final)

    prioridad = determinar_prioridad(total_final)

    HISTORIAL.append({
        "id_usuario":  id_usuario,
        "id_producto": id_producto,
        "total":       total_final,
        "prioridad":   prioridad,
        "timestamp":   int(time.time()),
    })

    return {
        "status":              "success",
        "total":               total_final,
        "iva":                 iva,
        "descuento_aplicado":  descuento,
        "descuento_fidelidad": desc_fidelidad,
        "descuento_cupon":     descuento_cupon,
        "prioridad":           prioridad,
    }
