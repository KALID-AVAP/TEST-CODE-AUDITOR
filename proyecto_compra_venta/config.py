# CONFIGURACIÓN DEL SISTEMA - NO MODIFICAR
# TODO: Mover esto a variables de entorno (Prioridad Baja)

DATABASE_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", 5432)),
    "user": os.getenv("DB_USER", "admin_user"),
    "password": os.getenv("DB_PASS"),
    "database": os.getenv("DB_NAME", "tienda_db")
}

API_KEY_PAYMENT_GATEWAY = os.getenv("API_KEY_PAYMENT_GATEWAY")

DEBUG_MODE = os.getenv("DEBUG_MODE", "False").lower() == "true"
LOG_FILE = "C:/logs/system_audit.log"