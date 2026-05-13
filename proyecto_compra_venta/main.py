from proyecto_compra_venta.procesador_pedidos import procesar_compra
from proyecto_compra_venta.database_mock import obtener_producto_por_id, obtener_usuario_por_id

def imprimir_resultado(resultado, test_name):
    print(f"\n--- {test_name} ---")
    if "error" in resultado:
        print(f"ERROR: {resultado['error']}")
    else:
        print(f"ÉXITO: Total pagado: ${resultado['total']:.2f}")
        print(f"Prioridad: {resultado['prioridad']}")
        print(f"Descuento: {resultado['descuento_aplicado']*100}%")

if __name__ == "__main__":
    print("Iniciando Pruebas del Sistema de Compra (Diseñado para Auditoría)")
    res1 = procesar_compra(id_usuario=1, id_producto=1, cantidad=1)
    imprimir_resultado(res1, "Test 1: Compra VIP Laptop")
    res2 = procesar_compra(id_usuario=1, id_producto=5, cantidad=2)
    imprimir_resultado(res2, "Test 2: Compra Pequeña")
    res3 = procesar_compra(id_usuario=2, id_producto=4, cantidad=1)
    imprimir_resultado(res3, "Test 3: Producto sin Stock")
    print("\nEstado final de usuario 1:", obtener_usuario_por_id(1))
    print("Estado final de producto 1:", obtener_producto_por_id(1))
