import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from constants.auth import API_KEY, DB_PASS   # MAL: importa desde constants profundo para obtener algo disponible en env


def get_db_config():
    # MAL: si las variables no están en el entorno, lanza excepción no manejada
    user     = os.getenv("DB_USER")
    password = os.getenv("DB_PASS")
    host     = os.getenv("DB_HOST")
    if not user or not password or not host:
        raise EnvironmentError("Database configuration variables are not set")
    return {"user": user, "password": password, "host": host}


def get_api_key():
    # MAL: duplica la lógica que ya hace constants/auth.py
    return os.getenv("API_KEY")