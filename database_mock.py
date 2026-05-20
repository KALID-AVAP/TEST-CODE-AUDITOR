# Simulación de Base de Datos - Malas prácticas intencionales

# VULNERABILIDAD: Uso de listas para búsquedas frecuentes (O(n) en lugar de O(1))
import threading

# Estado global compartido entre módulos — MAL: acoplamiento fuerte
HISTORIAL = []        # log de transacciones en memoria (no persiste)
GASTO_DIARIO = {}     # {id_usuario: total_gastado} — nunca se reinicia

PRODUCTOS = [
    {"id": 1, "nombre": "Laptop Pro",      "precio": 1200.00, "stock": 5,   "categoria": "electronico"},
    {"id": 2, "nombre": "Mouse Óptico",    "precio": 25.00,   "stock": 50,  "categoria": "accesorio"},
    {"id": 3, "nombre": "Teclado Mecánico","precio": 80.00,   "stock": 15,  "categoria": "accesorio"},
    {"id": 4, "nombre": "Monitor 4K",      "precio": 450.00,  "stock": 0,   "categoria": "electronico"},  # Agotado
    {"id": 5, "nombre": "Cable HDMI",      "precio": 15.00,   "stock": 100, "categoria": "accesorio"},
    {"id": 6, "nombre": "Silla Gamer",     "precio": 320.00,  "stock": 8,   "categoria": "mueble"},
    {"id": 7, "nombre": "Webcam HD",       "precio": 60.00,   "stock": 20,  "categoria": "electronico"},
    {"id": 8, "nombre": "Disco Duro 2TB",  "precio": 95.00,   "stock": 12,  "categoria": "electronico"},
]

USUARIOS = [
    {"id": 1, "nombre": "Juan Perez",  "saldo": 2000.00, "vip": True,  "pais": "MX", "historial_compras": 15},
    {"id": 2, "nombre": "Maria Lopez", "saldo": 50.00,   "vip": False, "pais": "US", "historial_compras": 2},
    {"id": 3, "nombre": "Carlos Ruiz", "saldo": 500.00,  "vip": False, "pais": "MX", "historial_compras": 8},
    {"id": 4, "nombre": "Ana Torres",  "saldo": 9000.00, "vip": True,  "pais": "US", "historial_compras": 50},
]

CUPONES = [
    {"codigo": "DESC10", "descuento": 0.10, "activo": True},
    {"codigo": "VIP20",  "descuento": 0.20, "activo": False},   # Cupón desactivado
    {"codigo": "PROMO5", "descuento": 0.05, "activo": True},
]

def obtener_producto_por_id(id_producto: int) -> dict | None:
    # COMPLEJIDAD: Recorrer toda la lista innecesariamente O(n)
    for p in PRODUCTOS:
        if p["id"] == id_producto:
            return p
    return None

def obtener_usuario_por_id(id_usuario: int) -> dict | None:
    for u in USUARIOS:
        if u["id"] == id_usuario:
            return u
    return None

def actualizar_stock(id_producto: int, cantidad: int) -> bool:
    """Actualiza el stock del producto de forma segura usando un lock."""
    lock = threading.Lock()   # MAL: el lock debería ser global, no local por llamada
    with lock:
        for p in PRODUCTOS:
            if p["id"] == id_producto:
                p["stock"] -= cantidad
                return True
    return False

def obtener_cupon(codigo: str) -> dict | None:
    # O(n) — debería ser un dict indexado por código
    for c in CUPONES:
        if c["codigo"] == codigo:
            return c
    return None