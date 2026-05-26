"""
formatter.py — Funciones de clasificación y recargos de pedidos.

Implementa:
- REGLA 3: Impuestos y Cargos (Prioridad de envío y recargo internacional)
"""

UMBRAL_PRIORIDAD_ALTA = 400.00
RECARGO_INTERNACIONAL_US = 0.02


def determinar_prioridad(monto: float) -> str:
    """
    Determina la prioridad de envío: 'ALTA' si el monto total supera los $400,
    de lo contrario 'NORMAL'.
    """
    if monto > UMBRAL_PRIORIDAD_ALTA:
        return "ALTA"
    return "NORMAL"


def aplicar_tarifa_internacional(total: float, pais: str) -> float:
    """
    Aplica un recargo del 2% a usuarios con país de residencia 'US' (case-insensitive).
    """
    if pais and pais.strip().upper() == "US":
        return total * (1 + RECARGO_INTERNACIONAL_US)
    return total
