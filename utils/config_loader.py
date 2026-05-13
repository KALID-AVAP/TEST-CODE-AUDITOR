import os
from ..constants.auth import API_KEY, DB_PASS

def get_db_config():
    # Obtén credenciales de variables de entorno
    return {
        "user": os.getenv("DB_USER", "admin_user"),
        "password": os.getenv("DB_PASS"),
        "host": os.getenv("DB_HOST", "localhost")
    }

def get_api_key():
    return os.getenv("API_KEY")