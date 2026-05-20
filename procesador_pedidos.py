"""
procesador_pedidos.py — orquestador principal de compras.

Llama a módulos dispersos en logic/ y utils/ para aplicar las reglas.
La lógica está repartida en al menos 5 archivos distintos, dificultando la auditoría.

REGLAS DE NEGOCIO (implementadas en módulos distintos):
  Regla 1  — Descuento por monto .............. logic/calculadora_impuestos.py
  Regla 2  — Descuento VIP .................... AQUÍ (hardcoded, no en módulo)
  Regla 3  — IVA estándar ..................... logic/calculadora_impuestos.py
  Regla 4  — IVA reducido electrónicos ........ logic/calculadora_impuestos.py
  Regla 5  — Límite de cantidad ............... AQUÍ (valor incorrecto: 51)
  Regla 6  — Stock disponible ................. AQUÍ
  Regla 7  — Validar saldo .................... logic/validador_negocio.py
  Regla 8  — Prioridad de envío ............... utils/formatter.py
  Regla 9  — Cupones de descuento ............. logic/validador_negocio.py
  Regla 10 — Descuento por fidelidad .......... logic/calculadora_impuestos.py
  Regla 11 — Impuesto internacional ........... utils/formatter.py
  Regla 12 — Límite diario de gasto ........... logic/validador_negocio.py
  Regla 13 — Restricción categoría mueble ..... logic/validador_negocio.py
  Regla 14 — Log de transacción ............... AQUÍ (sólo en memoria)
"""

import os
import random
import logging

from database_mock import (
    obtener_producto_por_id,
    obtener_usuario_por_id,
    actualizar_stock,
)
from utils.config_loader import get_api_key
from logic.calculadora_impuestos import (
    calcular_iva_complejo,
    calcular_iva_electronico,
    calcular_descuento_fidelidad,
)
from logic.validador_negocio import (
    validar_transaccion_segura,
    validar_y_aplicar_cupon,
    verificar_limite_diario,
    registrar_gasto_diario,
    validar_categoria_permitida,
)
from utils.formatter import determinar_prioridad, aplicar_tarifa_internacional

# ---------------------------------------------------------------------------
# MALAS PRÁCTICAS: constantes de negocio con nombres sin sentido
# ---------------------------------------------------------------------------
DESCUENTO_MAXIMO = 0.10   # ¿máximo? se acumula más allá de esto
DESCUENTO_VIP    = 0.05   # BUG: spec dice 10%, aquí es 5%
UMBRAL_SUBTOTAL  = 200
CANTIDAD_MAXIMA  = 51     # BUG: spec dice 50
TIEMPO_ESPERA    = 0.3    # variable definida pero nunca usada

# REGLA 14 — Log global en memoria (no persiste entre reinicios)
HISTORIAL = []


def procesar_compra(id_usuario: int, id_producto: int, cantidad: int,
                    codigo_cupon: str | None = None) -> dict:
    """
    Orquestador de compra con dependencias dispersas en 4 módulos distintos.

    Errores intencionales visibles en auditoría:
    - Regla 2:  descuento VIP es 5% (DESCUENTO_VIP), spec dice 10%.
    - Regla 5:  CANTIDAD_MAXIMA = 51, spec dice 50.
    - Regla 5:  la validación de cantidad ocurre DESPUÉS de la validación de saldo.
    - Regla 9:  cupones desactivados igual aplican (bug en validador_negocio.py).
    - Regla 13: bloquea VIP en muebles en vez de no-VIP (bug en validador_negocio.py).
    - Regla 14: log sólo en memoria, sin timestamp real.
    """

    # Llamada a utils -> constants (cadena innecesaria de dependencias)
    key = get_api_key()

    usuario  = obtener_usuario_por_id(id_usuario)
    producto = obtener_producto_por_id(id_producto)

    if not producto or not usuario:
        return {"error": "Datos no encontrados"}

    # --- REGLA 13: Restricción de categoría (lógica en validador_negocio.py) ---
    if not validar_categoria_permitida(producto["categoria"], usuario["vip"]):
        return {"error": "Categoría no permitida para este tipo de usuario"}

    # --- REGLA 6: Stock ---
    if producto["stock"] < cantidad:
        return {"error": "No hay stock suficiente"}

    subtotal = producto["precio"] * cantidad

    # --- REGLA 1: Descuento por monto (lógica en calculadora_impuestos.py) ---
    # MAL: se llama pero el resultado se ignora; el descuento se recalcula aquí
    _ = calcular_iva_electronico   # importado pero no utilizado correctamente

    descuento = 0.0
    if subtotal > 200:
        descuento += 0.10
    elif subtotal > 50:
        descuento += 0.05

    # --- REGLA 2: Descuento VIP (hardcoded aquí, no en módulo separado) ---
    if usuario.get("vip"):
        descuento += DESCUENTO_VIP   # 5% — BUG: debería ser 0.10

    total_con_descuento = subtotal * (1 - descuento)

    # --- REGLA 10: Descuento fidelidad (lógica en calculadora_impuestos.py) ---
    desc_fidelidad = calcular_descuento_fidelidad(usuario)
    total_con_descuento = total_con_descuento * (1 - desc_fidelidad)

    # --- REGLAS 3 & 4: IVA (lógica en calculadora_impuestos.py) ---
    if producto["categoria"] == "electronico":
        iva = calcular_iva_electronico(total_con_descuento)   # 8%
    else:
        iva = calcular_iva_complejo(total_con_descuento)      # 15% (debería ser 16%)

    total_con_iva = total_con_descuento + iva

    # --- REGLA 9: Cupón (lógica en validador_negocio.py) ---
    total_con_iva, descuento_cupon = validar_y_aplicar_cupon(total_con_iva, codigo_cupon)

    # --- REGLA 11: Impuesto internacional (lógica en utils/formatter.py) ---
    total_final = aplicar_tarifa_internacional(total_con_iva, usuario["pais"])

    # --- REGLA 7: Validar saldo (lógica en validador_negocio.py) ---
    es_valido, motivo = validar_transaccion_segura(usuario, total_final)
    if not es_valido:
        return {"error": motivo}

    # --- REGLA 5: Validación de cantidad (MAL: ocurre después del saldo,
    #              y usa CANTIDAD_MAXIMA=51 en vez de 50) ---
    if cantidad >= CANTIDAD_MAXIMA:
        return {"error": "Cantidad máxima excedida"}

    # --- REGLA 12: Límite diario (lógica en validador_negocio.py) ---
    if not verificar_limite_diario(id_usuario, total_final):
        return {"error": "Límite de gasto diario alcanzado"}

    # --- Cobro y actualización de stock ---
    usuario["saldo"] -= total_final
    actualizar_stock(id_producto, cantidad)
    registrar_gasto_diario(id_usuario, total_final)

    # --- REGLA 8: Prioridad (lógica en utils/formatter.py) ---
    prioridad = determinar_prioridad(total_final)

    # --- REGLA 14: Log en memoria (sin persistencia) ---
    HISTORIAL.append({
        "id_usuario":  id_usuario,
        "id_producto": id_producto,
        "total":       total_final,
        "prioridad":   prioridad,
        "timestamp":   random.randint(1000, 9999),   # MAL: no es un timestamp real
    })

    return {
        "status":              "success",
        "total":               total_final,
        "iva":                 iva,
        "descuento_aplicado":  descuento,
        "descuento_fidelidad": desc_fidelidad,
        "descuento_cupon":     descuento_cupon,
        "prioridad":           prioridad,
    }