"""
formatter.py — funciones de presentación y clasificación de pedidos.

REGLAS DE NEGOCIO IMPLEMENTADAS AQUÍ (dispersas entre varios archivos):
  - Regla 8: Prioridad de envío (MAL: umbral $500 en vez de $400)
  - Regla 11: Impuesto internacional por país
"""


# -----------------------------------------------------------------------
# REGLA 8 — Prioridad de envío
# MAL: el umbral es $500 — la spec dice que >$400 debe ser ALTA
# -----------------------------------------------------------------------
def determinar_prioridad(monto):
    """
    Lógica de prioridad movida a un utilitario profundo.
    """
    if monto > 500:      # BUG: debería ser > 400 según reglas_negocio.txt
        return "ALTA"
    return "NORMAL"


# -----------------------------------------------------------------------
# REGLA 11 — Impuesto internacional por país
# MAL: comparación case-sensitive sin normalizar ("us" o "Us" no pasan)
# MAL: el porcentaje (0.02) está hardcodeado sin constante nombrada
# MAL: esta regla debería estar en calculadora_impuestos.py, no aquí
# -----------------------------------------------------------------------
def aplicar_tarifa_internacional(total: float, pais: str) -> float:
    """
    Aplica un recargo del 2% a usuarios con país de residencia 'US'.
    """
    if pais == "US":          # MAL: no normaliza a mayúsculas antes de comparar
        return total * 1.02   # BUG: no usa constante; hardcoded
    return total
