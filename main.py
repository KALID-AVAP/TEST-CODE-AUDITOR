import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from procesador_pedidos import procesar_compra, HISTORIAL
from database_mock import obtener_producto_por_id, obtener_usuario_por_id


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


if __name__ == "__main__":
    print("=" * 55)
    print("  Sistema de Compra-Venta - Suite de Pruebas (Auditoria)")
    print("=" * 55)

    # Test 1: VIP compra Laptop — IVA reducido + descuento VIP
    res1 = procesar_compra(id_usuario=1, id_producto=1, cantidad=1)
    imprimir_resultado(res1, "Test 1: VIP compra Laptop Pro")

    # Test 2: Compra pequeña con cupon activo
    res2 = procesar_compra(id_usuario=1, id_producto=5, cantidad=2, codigo_cupon="PROMO5")
    imprimir_resultado(res2, "Test 2: Compra pequena con cupon PROMO5")

    # Test 3: Producto sin stock
    res3 = procesar_compra(id_usuario=2, id_producto=4, cantidad=1)
    imprimir_resultado(res3, "Test 3: Producto sin stock (Monitor 4K)")

    # Test 4: Usuario sin saldo suficiente
    res4 = procesar_compra(id_usuario=2, id_producto=1, cantidad=1)
    imprimir_resultado(res4, "Test 4: Usuario sin saldo (Maria Lopez -> Laptop)")

    # Test 5: Cupon desactivado - BUG: igual se aplica
    res5 = procesar_compra(id_usuario=1, id_producto=3, cantidad=2, codigo_cupon="VIP20")
    imprimir_resultado(res5, "Test 5: Cupon DESACTIVADO VIP20 (bug: aplica igual)")

    # Test 6: Restriccion de mueble - BUG: bloquea VIP en vez de no-VIP
    res6 = procesar_compra(id_usuario=1, id_producto=6, cantidad=1)
    imprimir_resultado(res6, "Test 6: VIP compra mueble (bug: deberia poder, pero se bloquea)")

    res6b = procesar_compra(id_usuario=3, id_producto=6, cantidad=1)
    imprimir_resultado(res6b, "Test 6b: No-VIP compra mueble (bug: deberia bloquearse, pero pasa)")

    # Test 7: Usuario de USA paga impuesto extra
    res7 = procesar_compra(id_usuario=4, id_producto=2, cantidad=3)
    imprimir_resultado(res7, "Test 7: Usuario USA paga impuesto internacional")

    # Test 8: Limite de cantidad — 50 pasa, 51 falla
    res8a = procesar_compra(id_usuario=4, id_producto=5, cantidad=50)
    imprimir_resultado(res8a, "Test 8a: Cantidad 50 (debe pasar)")

    res8b = procesar_compra(id_usuario=4, id_producto=5, cantidad=51)
    imprimir_resultado(res8b, "Test 8b: Cantidad 51 (debe fallar)")

    print("\n--- Estado final ---")
    print("Usuario 1 (Juan):", obtener_usuario_por_id(1))
    print("Usuario 4 (Ana): ", obtener_usuario_por_id(4))
    print("Producto 1 stock:", obtener_producto_por_id(1))
    print(f"Entradas en HISTORIAL: {len(HISTORIAL)}")
