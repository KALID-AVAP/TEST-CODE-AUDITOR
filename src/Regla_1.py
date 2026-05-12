from utils import sumar, obtener_usuario
from auth import login, generar_token
from db import ejecutar_query
import os

def main():
    usuario = obtener_usuario(1)
    total = sumar(5, 10, 15)
    token = generar_token('admin')
    print(f'Token: {token}')
    print(f'Usuario: {usuario}')
    print(f'Total: {total}')

if __name__ == '__main__':
    main()
