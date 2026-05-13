import os
from ..constants.auth import API_KEY, DB_PASS

def get_db_config():
    # Obtén credenciales de variables de entorno, sin valores por defecto
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASS")
    host = os.getenv("DB_HOST")
    if not user or not password or not host:
        raise EnvironmentError("Database configuration variables are not set")
    return {
        "user": user,
        "password": password,
        "host": host
    }

def get_api_key():
    return os.getenv("API_KEY")