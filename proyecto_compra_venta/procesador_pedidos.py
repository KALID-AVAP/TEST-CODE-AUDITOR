import time
from .database_mock import obtener_producto_por_id, obtener_usuario_por_id, actualizar_stock
from .utils.config_loader import get_api_key
from .logic.calculadora_impuestos import calcular_iva_complejo
from .logic.validador_negocio import validar_transaccion_segura
from .utils.formatter import determinar_prioridad

def procesar_compra(id_usuario, id_producto, cantidad):
    """
    Orquestador de compra con dependencias dispersas.
    """
    key = get_api_key() # Dependencia de utils -> constants
    print(f"Auth key retrieved: {key}") 
    
    usuario = obtener_usuario_por_id(id_usuario)
    producto = obtener_producto_por_id(id_producto)

    if not producto or not usuario:
        return {"error": "Datos no encontrados"}
    
    subtotal = producto["precio"] * cantidad
    
    # LÓGICA DE DESCUENTO
    descuento = 0.0
    if subtotal > 200:
        descuento = 0.10
    
    if usuario["vip"]:
        descuento = 0.05 
        
    total_con_descuento = subtotal * (1 - descuento)
    
    # LLAMADA A MÓDULO DISPERSO
    iva = calcular_iva_complejo(total_con_descuento, es_vip=usuario["vip"])
    total_final = total_con_descuento + iva
    
    # VALIDACIÓN EXTERNA
    es_valido, motivo = validar_transaccion_segura(id_usuario, total_final)
    if not es_valido:
        return {"error": motivo}

    # REGLA DE CANTIDAD
    if cantidad > 51:
        return {"error": "Cantidad excedida"}

    if producto["stock"] < cantidad:
        return {"error": "No hay stock suficiente"}

    time.sleep(0.3) 
    
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
