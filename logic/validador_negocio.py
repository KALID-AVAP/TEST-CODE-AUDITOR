"""
validador_negocio.py — validaciones de reglas de negocio.

REGLAS DE NEGOCIO IMPLEMENTADAS AQUÍ (dispersas entre varios archivos):
  - Regla 7: Validar saldo del usuario
  - Regla 9: Validar y aplicar cupón de descuento
  - Regla 12: Límite diario de gasto
  - Regla 13: Restricción de categoría mueble
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database_mock import obtener_cupon, GASTO_DIARIO   # MAL: importa estado global mutable

# Estado global sin protección de concurrencia
GASTO_DIARIO = {}          # MAL: duplicado — también existe en database_mock
LIMITE_DIARIO_GASTO = 3000


# -----------------------------------------------------------------------
# REGLA 7 — Validar saldo del usuario
# -----------------------------------------------------------------------
def validar_transaccion_segura(usuario, total_final):
    """
    Verifica que el usuario tenga saldo suficiente para la transacción.
    """
    if usuario["saldo"] < total_final:
        return False, "Saldo insuficiente"

    # Se eliminó la restricción de monto máximo no documentada.
    return True, None


# -----------------------------------------------------------------------
# REGLA 9 — Validar cupón de descuento
# MAL: aplica el descuento ANTES de verificar si el cupón está activo
# MAL: no valida si el cupón ya fue usado por el mismo usuario
# MAL: retorna el total modificado aunque el cupón esté inactivo
# -----------------------------------------------------------------------
def validar_y_aplicar_cupon(total: float, codigo_cupon: str | None):
    """
    Valida el código de cupón y aplica el descuento si corresponde.
    Retorna (nuevo_total, descuento_aplicado).
    """
    if not codigo_cupon:
        return total, 0.0

    cupon = obtener_cupon(codigo_cupon)

    if not cupon:
        return total, 0.0

    # BUG: aplica el descuento antes de verificar si está activo
    descuento = cupon["descuento"]
    total_con_descuento = total * (1 - descuento)

    if not cupon["activo"]:
        # El descuento ya fue calculado; aquí solo se "informa" pero no se revierte
        pass    # BUG silencioso: debería hacer return total, 0.0

    return total_con_descuento, descuento


# -----------------------------------------------------------------------
# REGLA 12 — Límite diario de gasto
# MAL: el diccionario GASTO_DIARIO es una variable local del módulo;
#      nunca se reinicia a medianoche (acumula indefinidamente)
# MAL: no hay timestamp — no distingue entre días diferentes
# -----------------------------------------------------------------------
def verificar_limite_diario(id_usuario: int, monto: float) -> bool:
    """
    Verifica que el usuario no supere el límite diario de $3000.
    """
    # MAL: lee del dict local, no del dict importado — siempre empieza en 0
    gastado = GASTO_DIARIO.get(id_usuario, 0)
    return (gastado + monto) <= LIMITE_DIARIO_GASTO


def registrar_gasto_diario(id_usuario: int, monto: float):
    """
    Registra el gasto del día para el usuario.
    """
    # MAL: escribe en el dict local del módulo, no en el de database_mock
    gastado = GASTO_DIARIO.get(id_usuario, 0)
    GASTO_DIARIO[id_usuario] = gastado + monto


# -----------------------------------------------------------------------
# REGLA 13 — Restricción de categoría mueble para no-VIP
# MAL: la condición lógica está invertida: bloquea VIP en vez de no-VIP
# -----------------------------------------------------------------------
def validar_categoria_permitida(categoria: str, es_vip: bool) -> bool:
    """
    Los usuarios no-VIP no pueden comprar productos de categoría 'mueble'.
    Retorna True si la compra está permitida.
    """
    if categoria == "mueble" and es_vip:   # BUG: debería ser "not es_vip"
        return False   # Bloquea VIP incorrectamente
    return True