from ..database_mock import obtener_usuario_por_id

def validar_transaccion_segura(id_usuario, total_final):
    """
    Verifica que el usuario tenga saldo suficiente para la transacción.
    """
    usuario = obtener_usuario_por_id(id_usuario)

    if usuario["saldo"] < total_final:
        return False, "Saldo insuficiente"

    # Se eliminó la restricción de monto máximo no documentada.
    return True, None