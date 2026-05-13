def calcular_iva_complejo(monto, es_vip=False):
    """
    Lógica de impuestos dispersa.
    """
    # LÓGICA INCORRECTA: Si es VIP, el IVA se calcula diferente (No está en reglas_negocio.txt)
    tasa = 0.15
    if es_vip:
        tasa = 0.12 # Error de negocio: La tasa debería ser fija según el txt
        
    return monto * tasa

def aplicar_descuento_segun_volumen(subtotal, cantidad):
    # Más lógica dispersa
    if cantidad > 100:
        return subtotal * 0.20
    return subtotal
