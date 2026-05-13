# Simulación de Base de Datos - Malas prácticas intencionales

# VULNERABILIDAD: Uso de listas para búsquedas frecuentes (O(n) en lugar de O(1))
PRODUCTOS = [
    {"id": 1, "nombre": "Laptop Pro", "precio": 1200.00, "stock": 5},
    {"id": 2, "nombre": "Mouse Óptico", "precio": 25.00, "stock": 50},
    {"id": 3, "nombre": "Teclado Mecánico", "precio": 80.00, "stock": 15},
    {"id": 4, "nombre": "Monitor 4K", "precio": 450.00, "stock": 0}, # Agotado
    {"id": 5, "nombre": "Cable HDMI", "precio": 15.00, "stock": 100}
]

USUARIOS = [
    {"id": 1, "nombre": "Juan Perez", "saldo": 2000.00, "vip": True},
    {"id": 2, "nombre": "Maria Lopez", "saldo": 50.00, "vip": False}
]

def obtener_producto_por_id(id_producto):
    # COMPLEJIDAD: Recorrer toda la lista innecesariamente
    for p in PRODUCTOS:
        if p["id"] == id_producto:
            return p
    return None

def obtener_usuario_por_id(id_usuario):
    for u in USUARIOS:
        if u["id"] == id_usuario:
            return u
    return None

def actualizar_stock(id_producto, cantidad):
    # Malas prácticas: Modificación directa de estructuras globales sin lock/validación robusta
    for p in PRODUCTOS:
        if p["id"] == id_producto:
            p["stock"] -= cantidad
            return True
    return False
