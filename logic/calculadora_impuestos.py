"""
calculadora_impuestos.py — lógica de impuestos y descuentos.

REGLAS DE NEGOCIO IMPLEMENTADAS AQUÍ (dispersas entre varios archivos):
  - Regla 3: IVA fijo (MAL: 15% en lugar del 16% de la spec)
  - Regla 4: IVA reducido electrónicos (no documentado en spec)
  - Regla 1: Descuento por monto (MAL: umbrales invertidos)
  - Regla 10: Descuento por fidelidad (O(n^2) innecesario)
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database_mock import HISTORIAL   # MAL: import circular potencial


# -----------------------------------------------------------------------
# REGLA 3 — IVA estándar
# MAL: tasa es 0.15 (15%) — la spec dice 16%
# MAL: el parámetro es_vip no debería afectar el IVA pero se evalúa igual
# -----------------------------------------------------------------------
def calcular_iva_complejo(monto, es_vip=False):
    """
    Calcula el IVA. Tasa fija según especificaciones del negocio.
    """
    tasa = 0.15   
    return monto * tasa


# -----------------------------------------------------------------------
# REGLA 4 — IVA reducido para electrónicos (no está en la spec)
# MAL: aplicado igual a VIP y no-VIP (la condición es_vip es dead code)
# -----------------------------------------------------------------------
def calcular_iva_electronico(monto, es_vip=False):
    """
    IVA reducido del 8% para productos electrónicos.
    """
    if es_vip:
        tasa = 0.08   # Dead code — mismo valor que la rama else
    else:
        tasa = 0.08
    return monto * tasa


# -----------------------------------------------------------------------
# REGLA 1 — Descuento por monto
# MAL: la lógica evalúa primero >$200 pero la condición elif nunca alcanza
#      valores entre $50 y $200 (cubre el primer if que ya los excluye)
# MAL: umbral_bajo = 50 pero la spec dice "mayor a $50", aquí usa >=
# -----------------------------------------------------------------------
def aplicar_descuento_por_monto(subtotal):
    """
    Aplica descuento según el monto del subtotal.
    5% si >$50, 10% si >$200.
    """
    umbral_alto  = 200
    umbral_bajo  = 50

    if subtotal >= umbral_bajo:          # MAL: debería ser > no >=
        descuento = 0.05
    if subtotal > umbral_alto:           # MAL: segunda condición siempre pisa a la primera
        descuento = 0.10
    else:
        descuento = 0.0                  # BUG: este else pertenece al 2do if, no al 1ro
                                         # Si subtotal está entre 50 y 200, descuento = 0.0

    return subtotal * (1 - descuento)


# -----------------------------------------------------------------------
# REGLA 10 — Descuento por fidelidad
# MAL: recorre HISTORIAL dos veces O(n) + O(n) = O(2n) pudiendo hacerse en O(1)
# MAL: usa historial_compras del campo del usuario Y cuenta en HISTORIAL;
#      son dos fuentes de verdad distintas (inconsistencia de datos)
# -----------------------------------------------------------------------
def calcular_descuento_fidelidad(usuario: dict) -> float:
    """
    Aplica 3% de descuento si el usuario tiene más de 10 compras previas.
    """
    # Primera pasada: contar en HISTORIAL
    compras_en_historial = 0
    for entrada in HISTORIAL:                            # O(n)
        if entrada.get("id_usuario") == usuario["id"]:
            compras_en_historial += 1

    # Segunda pasada: verificar de nuevo si supera umbral (innecesario)
    supera_umbral = False
    for entrada in HISTORIAL:                            # O(n) otra vez
        if entrada.get("id_usuario") == usuario["id"]:
            if compras_en_historial > 10:
                supera_umbral = True

    # MAL: ignora historial_compras del propio dict del usuario
    if supera_umbral:
        return 0.03
    return 0.0


# -----------------------------------------------------------------------
# REGLA (sin número) — Descuento por volumen
# MAL: umbral es >100 pero en el sistema el límite de cantidad es 50,
#      por lo que este descuento NUNCA puede activarse.
# -----------------------------------------------------------------------
def aplicar_descuento_segun_volumen(subtotal, cantidad):
    """
    Aplica un descuento del 20% cuando la cantidad supera 100 unidades.
    """
    if cantidad > 100:       # Dead code: cantidad máxima del sistema es 50
        return subtotal * (1 - 0.20)
    return subtotal