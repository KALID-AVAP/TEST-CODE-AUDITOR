def determinar_prioridad(monto):
    """
    Lógica de prioridad movida a un utilitario profundo.
    """
    if monto > 500:
        return "ALTA"
    return "NORMAL"
