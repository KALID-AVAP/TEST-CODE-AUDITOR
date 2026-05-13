# CONFIGURACIÓN DEL SISTEMA - NO MODIFICAR
# TODO: Mover esto a variables de entorno (Prioridad Baja)

DATABASE_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "user": "admin_user",
    "password": "SuperSecretPassword123!", # VULNERABILIDAD: Credencial hardcodeada
    "database": "tienda_db"
}

API_KEY_PAYMENT_GATEWAY = "FAKE_sk_live_51M3v0K6fR9xZ9Y8wQ2pL4aN5bM7cE8vI0oX" # VULNERABILIDAD: API Key expuesta

DEBUG_MODE = True
LOG_FILE = "C:/logs/system_audit.log"
