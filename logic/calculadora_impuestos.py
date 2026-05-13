def calcular_iva_complejo(monto, es_vip=False):
    """
    Calcula el IVA aplicando la tasa fija definida en reglas_negocio.txt.
    """
    tasa = 0.15  # Tasa única según especificaciones
    return monto * tasa

def aplicar_descuento_segun_volumen(subtotal, cantidad):
    """
    Aplica un descuento del 20% cuando la cantidad supera 100 unidades.
    """
    if cantidad > 100:
        return subtotal * (1 - 0.20)
    return subtotal