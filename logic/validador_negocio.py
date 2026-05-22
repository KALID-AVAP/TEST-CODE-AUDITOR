"""
validador_negocio.py — validaciones de reglas de negocio corregidas.
"""

from database_mock import obtener_cupon, GASTO_DIARIO

LIMITE_DIARIO_GASTO = 3000

 def validar_transaccion_segura(usuario: dict, total_final: float) -> (bool, str | None):
    """
    Verifica que el usuario tenga saldo suficiente para la transacción.
    """
    if usuario.get("saldo", 0) < total_final:
        return False, "Saldo insuficiente"
    return True, None

 def validar_y_aplicar_cupon(total: float, codigo_cupon: str | None) -> (float, float):
    """
    Valida el código de cupón y aplica el descuento si corresponde.
    Retorna (nuevo_total, descuento_aplicado).
    """
    if not codigo_cupon:
        return total, 0.0
    cupon = obtener_cupon(codigo_cupon)
    if not cupon or not cupon.get("activo", False):
        return total, 0.0
    descuento = cupon["descuento"]
    total_con_descuento = total * (1 - descuento)
    return total_con_descuento, descuento

 def verificar_limite_diario(id_usuario: int, monto: float) -> bool:
    """
    Verifica que el usuario no supere el límite diario de $3000.
    """
    gastado = GASTO_DIARIO.get(id_usuario, 0)
    return (gastado + monto) <= LIMITE_DIARIO_GASTO

 def registrar_gasto_diario(id_usuario: int, monto: float):
    """
    Registra el gasto del día para el usuario.
    """
    gastado = GASTO_DIARIO.get(id_usuario, 0)
    GASTO_DIARIO[id_usuario] = gastado + monto

 def validar_categoria_permitida(categoria: str, es_vip: bool) -> bool:
    """
    Los usuarios no-VIP no pueden comprar productos de categoría 'mueble'.
    Retorna True si la compra está permitida.
    """
    if categoria == "mueble" and not es_vip:
        return False
    return True