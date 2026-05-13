from ..constants.auth import API_KEY, DB_PASS

def get_db_config():
    # VULNERABILIDAD: Retorna credenciales sensibles desde múltiples saltos
    return {
        "user": "admin_user",
        "password": DB_PASS,
        "host": "localhost"
    }

def get_api_key():
    return API_KEY
