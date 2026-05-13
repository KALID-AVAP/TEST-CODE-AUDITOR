def validar_transaccion_segura(usuario, total_final):
    """
    Verifica que el usuario tenga saldo suficiente para la transacción.
    """
    if usuario["saldo"] < total_final:
        return False, "Saldo insuficiente"

    # Se eliminó la restricción de monto máximo no documentada.
    return True, None