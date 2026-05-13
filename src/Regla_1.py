from utils import sumar, obtener_usuario
from auth import generar_token
import os

def main():
    # Obtener ID de usuario desde variable de entorno o usar el predeterminado
    user_id = int(os.getenv('USER_ID', '1'))
    usuario = obtener_usuario(user_id)

    # Calcular total
    total = sumar(5, 10, 15)

    # Generar token para el usuario obtenido
    token = generar_token(str(usuario))

    # Registrar información sin exponer el token
    print(f'Usuario: {usuario}')
    print(f'Total: {total}')
    # El token puede ser utilizado internamente sin imprimirlo

if __name__ == '__main__':
    main()