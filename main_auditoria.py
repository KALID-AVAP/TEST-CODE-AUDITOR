import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from procesador_pedidos import procesar_compra, HISTORIAL
from database_mock import obtener_producto_por_id, obtener_usuario_por_id

TEST_CASES = [
    {
        "name": "Test 1: VIP compra Laptop Pro",
        "args": {"id_usuario": 1, "id_producto": 1, "cantidad": 1},
        "expected_status": "success",
        "expected_note": "Debería regresar éxito con descuento VIP aplicado y cálculo de IVA.",
    },
    {
        "name": "Test 2: Compra pequena con cupon PROMO5",
        "args": {"id_usuario": 1, "id_producto": 5, "cantidad": 2, "codigo_cupon": "PROMO5"},
        "expected_status": "success",
        "expected_note": "Debería regresar éxito con el cupón activo aplicado.",
    },
    {
        "name": "Test 3: Producto sin stock (Monitor 4K)",
        "args": {"id_usuario": 2, "id_producto": 4, "cantidad": 1},
        "expected_status": "error",
        "expected_note": "Debería regresar un error por falta de stock.",
    },
    {
        "name": "Test 4: Usuario sin saldo (Maria Lopez -> Laptop)",
        "args": {"id_usuario": 2, "id_producto": 1, "cantidad": 1},
        "expected_status": "error",
        "expected_note": "Debería regresar un error por saldo insuficiente.",
    },
    {
        "name": "Test 5: Cupon DESACTIVADO VIP20 (bug: aplica igual)",
        "args": {"id_usuario": 1, "id_producto": 3, "cantidad": 2, "codigo_cupon": "VIP20"},
        "expected_status": "error",
        "expected_note": "Si la auditoría se hace bien, debería regresar un error o, al menos, no aplicar el cupón desactivado.",
    },
    {
        "name": "Test 6: VIP compra mueble (bug: deberia poder, pero se bloquea)",
        "args": {"id_usuario": 1, "id_producto": 6, "cantidad": 1},
        "expected_status": "success",
        "expected_note": "Si la auditoría se hace bien, debería regresar éxito: VIP debe poder comprar muebles.",
    },
    {
        "name": "Test 6b: No-VIP compra mueble (bug: deberia bloquearse, pero pasa)",
        "args": {"id_usuario": 3, "id_producto": 6, "cantidad": 1},
        "expected_status": "error",
        "expected_note": "Si la auditoría se hace bien, debería regresar un error: no-VIP no debe comprar muebles.",
    },
    {
        "name": "Test 7: Usuario USA paga impuesto internacional",
        "args": {"id_usuario": 4, "id_producto": 2, "cantidad": 3},
        "expected_status": "success",
        "expected_note": "Debería regresar éxito con recargo internacional aplicado.",
    },
    {
        "name": "Test 8a: Cantidad 50 (debe pasar)",
        "args": {"id_usuario": 4, "id_producto": 5, "cantidad": 50},
        "expected_status": "success",
        "expected_note": "Debería regresar éxito porque 50 es el límite permitido.",
    },
    {
        "name": "Test 8b: Cantidad 51 (debe fallar)",
        "args": {"id_usuario": 4, "id_producto": 5, "cantidad": 51},
        "expected_status": "error",
        "expected_note": "Debería regresar un error porque 51 supera el límite máximo.",
    },
]


def imprimir_resultado(resultado, test_name):
    print(f"\n--- {test_name} ---")
    if "error" in resultado:
        print(f"  ERROR: {resultado['error']}")
    else:
        print(f"  EXITO: Total pagado        : ${resultado['total']:.2f}")
        print(f"         Prioridad           : {resultado['prioridad']}")
        print(f"         Descuento aplicado  : {resultado['descuento_aplicado']*100:.0f}%")
        print(f"         Descuento fidelidad : {resultado['descuento_fidelidad']*100:.0f}%")
        print(f"         Descuento cupon     : {resultado['descuento_cupon']*100:.0f}%")
        print(f"         IVA                 : ${resultado['iva']:.2f}")


def auditar_resultado(resultado, expected_status, expected_note):
    actual_status = "error" if "error" in resultado else "success"
    passed = actual_status == expected_status
    print(f"  AUDITORÍA: {expected_note}")
    print(f"  Resultado esperado: {expected_status.upper()}")
    print(f"  Resultado real   : {actual_status.upper()}")
    print(f"  Estado de auditoría: {'OK' if passed else 'INCORRECTO'}")


if __name__ == "__main__":
    print("=" * 75)
    print("  Sistema de Compra-Venta - Main de Auditoría")
    print("=" * 75)

    for case in TEST_CASES:
        resultado = procesar_compra(**case["args"])
        imprimir_resultado(resultado, case["name"])
        auditar_resultado(resultado, case["expected_status"], case["expected_note"])

    print("\n--- Estado final ---")
    print("Usuario 1 (Juan):", obtener_usuario_por_id(1))
    print("Usuario 4 (Ana): ", obtener_usuario_por_id(4))
    print("Producto 1 stock:", obtener_producto_por_id(1))
    print(f"Entradas en HISTORIAL: {len(HISTORIAL)}")
