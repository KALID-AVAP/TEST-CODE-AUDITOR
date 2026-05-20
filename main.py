import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from procesador_pedidos import procesar_compra, HISTORIAL
from database_mock import obtener_producto_por_id, obtener_usuario_por_id

KNOWN_ISSUES = {
    "Test 1: VIP compra Laptop Pro":
        "Funciona: aplica descuento VIP y calcula IVA, pero el código aún usa ciertas reglas dispersas en varios módulos.",
    "Test 2: Compra pequena con cupon PROMO5":
        "Funciona: el cupón activo se aplica. Aun así, la validación del cupón en el módulo puede ser frágil si cambian las reglas de activación.",
    "Test 3: Producto sin stock (Monitor 4K)":
        "Funciona: detecta stock insuficiente. El comportamiento es correcto, aunque el acceso al inventario usa listas O(n).",
    "Test 4: Usuario sin saldo (Maria Lopez -> Laptop)":
        "Funciona: la validación de saldo detiene la transacción. La regla está bien, pero la lógica de orden puede ser mejorada.",
    "Test 5: Cupon DESACTIVADO VIP20 (bug: aplica igual)":
        "Incorrecto: el cupón desactivado no debería aplicarse. El sistema devuelve éxito incluso cuando la auditoría debería detectar y rechazar ese descuento.",
    "Test 6: VIP compra mueble (bug: deberia poder, pero se bloquea)":
        "Incorrecto: la regla de categoría está invertida en validador_negocio.py, bloqueando VIP en muebles cuando debería permitirlos.",
    "Test 6b: No-VIP compra mueble (bug: deberia bloquearse, pero pasa)":
        "Incorrecto: los usuarios no-VIP pueden comprar muebles, lo opuesto de la regla esperada.",
    "Test 7: Usuario USA paga impuesto internacional":
        "Funciona: aplica recargo internacional. Sin embargo, la comparación de país es case-sensitive y el porcentaje está hardcodeado.",
    "Test 8a: Cantidad 50 (debe pasar)":
        "Funciona: el límite aceptado es 50 y la compra se procesa correctamente.",
    "Test 8b: Cantidad 51 (debe fallar)":
        "Funciona: la validación de cantidad rechaza 51. Esto es correcto según la regla de negocio.",
}


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

    observacion = KNOWN_ISSUES.get(test_name)
    if observacion:
        print(f"  NOTA: {observacion}")


if __name__ == "__main__":
    print("=" * 55)
    print("  Sistema de Compra-Venta - Suite de Pruebas (Funciona pero con problemas conocidos)")
    print("=" * 55)

    res1 = procesar_compra(id_usuario=1, id_producto=1, cantidad=1)
    imprimir_resultado(res1, "Test 1: VIP compra Laptop Pro")

    res2 = procesar_compra(id_usuario=1, id_producto=5, cantidad=2, codigo_cupon="PROMO5")
    imprimir_resultado(res2, "Test 2: Compra pequena con cupon PROMO5")

    res3 = procesar_compra(id_usuario=2, id_producto=4, cantidad=1)
    imprimir_resultado(res3, "Test 3: Producto sin stock (Monitor 4K)")

    res4 = procesar_compra(id_usuario=2, id_producto=1, cantidad=1)
    imprimir_resultado(res4, "Test 4: Usuario sin saldo (Maria Lopez -> Laptop)")

    res5 = procesar_compra(id_usuario=1, id_producto=3, cantidad=2, codigo_cupon="VIP20")
    imprimir_resultado(res5, "Test 5: Cupon DESACTIVADO VIP20 (bug: aplica igual)")

    res6 = procesar_compra(id_usuario=1, id_producto=6, cantidad=1)
    imprimir_resultado(res6, "Test 6: VIP compra mueble (bug: deberia poder, pero se bloquea)")

    res6b = procesar_compra(id_usuario=3, id_producto=6, cantidad=1)
    imprimir_resultado(res6b, "Test 6b: No-VIP compra mueble (bug: deberia bloquearse, pero pasa)")

    res7 = procesar_compra(id_usuario=4, id_producto=2, cantidad=3)
    imprimir_resultado(res7, "Test 7: Usuario USA paga impuesto internacional")

    res8a = procesar_compra(id_usuario=4, id_producto=5, cantidad=50)
    imprimir_resultado(res8a, "Test 8a: Cantidad 50 (debe pasar)")

    res8b = procesar_compra(id_usuario=4, id_producto=5, cantidad=51)
    imprimir_resultado(res8b, "Test 8b: Cantidad 51 (debe fallar)")

    print("\n--- Estado final ---")
    print("Usuario 1 (Juan):", obtener_usuario_por_id(1))
    print("Usuario 4 (Ana): ", obtener_usuario_por_id(4))
    print("Producto 1 stock:", obtener_producto_por_id(1))
    print(f"Entradas en HISTORIAL: {len(HISTORIAL)}")
