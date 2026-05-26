"""
validador_negocio.py — Validaciones de reglas de negocio.

Implementa:
- REGLA 1: Validación de Pedido y Disponibilidad (Categorías, Stock)
- REGLA 4: Seguridad de Pago y Auditoría (Saldo, Límite de Gasto Diario)
"""

import os
import sys
import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database_mock import obtener_cupon, HISTORIAL

LIMITE_DIARIO_GASTO = 3000.00


def validar_transaccion_segura(usuario: dict, total_final: float) -> tuple[bool, str | None]:
    """
    Verifica que el usuario tenga saldo suficiente para completar la transacción.
    """
    if usuario["saldo"] < total_final:
        return False, "Saldo insuficiente"
    return True, None


def validar_y_aplicar_cupon(total: float, codigo_cupon: str | None, id_usuario: int) -> tuple[float, float]:
    """
    Valida el código de cupón y aplica el descuento si corresponde.
    Rechaza cupones inactivos o ya usados por el mismo usuario.
    Retorna (nuevo_total, descuento_aplicado).
    
    Lanza ValueError si el cupón no es válido o está inactivo/usado.
    """
    if not codigo_cupon:
        return total, 0.0

    cupon = obtener_cupon(codigo_cupon)
    if not cupon:
        raise ValueError("Cupón no encontrado")

    if not cupon["activo"]:
        raise ValueError("El cupón ingresado está desactivado")

    # Verificar si el usuario ya usó este cupón en su historial
    for entrada in HISTORIAL:
        if entrada.get("id_usuario") == id_usuario and entrada.get("codigo_cupon") == codigo_cupon:
            raise ValueError("El cupón ya ha sido utilizado por este usuario")

    descuento = cupon["descuento"]
    nuevo_total = total * (1 - descuento)
    return nuevo_total, descuento


def verificar_limite_diario(id_usuario: int, monto: float) -> bool:
    """
    Verifica que el usuario no supere el límite diario de $3000 en el día calendario actual.
    """
    hoy = datetime.date.today()
    gastado_hoy = 0.0
    
    for entrada in HISTORIAL:
        if entrada.get("id_usuario") == id_usuario:
            ts = entrada.get("timestamp")
            if ts:
                fecha_entrada = datetime.date.fromtimestamp(ts)
                if fecha_entrada == hoy:
                    gastado_hoy += entrada.get("total", 0.0)
                    
    return (gastado_hoy + monto) <= LIMITE_DIARIO_GASTO


def registrar_gasto_diario(id_usuario: int, monto: float):
    """
    Registra el gasto. Al utilizar un cálculo dinámico basado en HISTORIAL,
    esta función queda para compatibilidad con la estructura original.
    """
    pass


def validar_categoria_permitida(categoria: str, es_vip: bool) -> bool:
    """
    Los usuarios no-VIP no pueden comprar productos de la categoría 'mueble'.
    Los usuarios VIP pueden comprar cualquier categoría.
    """
    if categoria == "mueble" and not es_vip:
        return False
    return True