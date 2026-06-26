"""
calculadora_impuestos.py — Lógica de impuestos y descuentos.

Implementa:
- REGLA 2: Cálculo de Descuentos (por monto, VIP, fidelidad)
- REGLA 3: Cálculo de Impuestos (IVA estándar de 12% e IVA reducido de 7%)
"""

from database_mock import HISTORIAL

# Constantes de Impuestos y Descuentos
IVA_ESTANDAR = 0.12      # 12% según spec de Regla 3
IVA_REDUCIDO = 0.07      # 7% para electrónicos según spec de Regla 3

DESCUENTO_MONTO_BAJO = 0.05  # 5% si > $50
DESCUENTO_MONTO_ALTO = 0.10  # 10% si > $200
UMBRAL_BAJO = 50.00
UMBRAL_ALTO = 200.00

DESCUENTO_VIP = 0.10         # 10% adicional acumulativo
DESCUENTO_FIDELIDAD = 0.03    # 3% adicional acumulativo
UMBRAL_FIDELIDAD_COMPRAS = 10


def calcular_iva_complejo(monto: float) -> float:
    """
    Calcula el IVA estándar del 12% sobre el monto.
    """
    return monto * IVA_ESTANDAR


def calcular_iva_electronico(monto: float) -> float:
    """
    Calcula el IVA reducido del 7% sobre el monto para electrónicos.
    """
    return monto * IVA_REDUCIDO


def aplicar_descuento_por_monto(subtotal: float) -> float:
    """
    Aplica descuento automático no acumulativo basado en el subtotal:
    5% si > $50.00, o 10% si > $200.00 (el mayor reemplaza al menor).
    """
    if subtotal > UMBRAL_ALTO:
        descuento = DESCUENTO_MONTO_ALTO
    elif subtotal > UMBRAL_BAJO:
        descuento = DESCUENTO_MONTO_BAJO
    else:
        descuento = 0.0
    return subtotal * (1 - descuento)


def obtener_porcentaje_descuento_monto(subtotal: float) -> float:
    """
    Retorna el porcentaje de descuento aplicable por monto de subtotal.
    """
    if subtotal > UMBRAL_ALTO:
        return DESCUENTO_MONTO_ALTO
    elif subtotal > UMBRAL_BAJO:
        return DESCUENTO_MONTO_BAJO
    return 0.0


def calcular_descuento_fidelidad(usuario: dict) -> float:
    """
    Aplica 3% de descuento adicional si el usuario supera las 10 compras previas en total
    (historial previo + historial de la sesión actual en HISTORIAL).
    """
    compras_previas = usuario.get("historial_compras", 0)
    compras_sesion = sum(1 for entrada in HISTORIAL if entrada.get("id_usuario") == usuario["id"])

    if (compras_previas + compras_sesion) > UMBRAL_FIDELIDAD_COMPRAS:
        return DESCUENTO_FIDELIDAD
    return 0.0