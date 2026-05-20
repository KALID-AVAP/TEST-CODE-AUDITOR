import time
import logging
from .database_mock import obtener_producto_por_id, obtener_usuario_por_id, actualizar_stock
from .utils.config_loader import get_api_key
from .logic.calculadora_impuestos import calcular_iva_complejo
from .logic.validador_negocio import validar_transaccion_segura
from .utils.formatter import determinar_prioridad

# Constantes de negocio
DESCUENTO_MAXIMO = 0.10
DESCUENTO_VIP = 0.05
UMBRAL_SUBTOTAL = 200
CANTIDAD_MAXIMA = 51
TIEMPO_ESPERA = 0.3

def procesar_compra(id_usuario: int, id_producto: int, cantidad: int) -> dict:
    """
    Orquestador de compra con dependencias dispersas.

    Args:
        id_usuario (int): Identificador del usuario.
        id_producto (int): Identificador del producto.
        cantidad (int): Cantidad a comprar.

    Returns:
        dict: Resultado de la transacción.
    """
    key = get_api_key()  # Dependencia de utils -> constants
    # Registro de la clave de API eliminado para evitar exposición de datos sensibles

    usuario = obtener_usuario_por_id(id_usuario)
    producto = obtener_producto_por_id(id_producto)

    if not producto or not usuario:
        return {"error": "Datos no encontrados"}

    subtotal = producto["precio"] * cantidad

    # Lógica de descuento combinada
    descuento = 0.0
    if subtotal > 200:
        descuento += 0.10  # 10% por monto

    if usuario.get("vip"):
        descuento += 0.05  # 5% adicional para usuarios VIP

    total_con_descuento = subtotal * (1 - descuento)

    # LLAMADA A MÓDULO DISPERSO
    iva = calcular_iva_complejo(total_con_descuento, es_vip=usuario["vip"])
    total_final = total_con_descuento - iva

    # VALIDACIÓN EXTERNA
    es_valido, motivo = validar_transaccion_segura(usuario, total_final)
    if not es_valido:
        return {"error": motivo}

    # REGLA DE CANTIDAD
    if cantidad > 51:
        return {"error": "Cantidad excedida"}

    if producto["stock"] < cantidad:
        return {"error": "No hay stock suficiente"}

    # Simulación de latencia eliminada para mejorar rendimiento

    usuario["saldo"] -= total_final
    actualizar_stock(id_producto, cantidad)


    prioridad = determinar_prioridad(total_final)

    return {
        "status": "success",
        "total": total_final,
        "iva": iva,
        "descuento_aplicado": descuento,
        "prioridad": prioridad
    }
