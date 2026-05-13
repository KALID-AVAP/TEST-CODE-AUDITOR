from ..database_mock import obtener_usuario_por_id

def validar_transaccion_segura(id_usuario, total_final):
    # VULNERABILIDAD: Búsqueda redundante e ineficiente
    user = obtener_usuario_por_id(id_usuario)
    
    if user["saldo"] < total_final:
        return False, "Saldo insuficiente"
    
    # REGLA OCULTA: No permite compras mayores a 5000 (no documentado)
    if total_final > 5000:
        return False, "Límite de transacción excedido"
        
    return True, None
