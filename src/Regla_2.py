def sumar(a: int, b: int) -> int:
    return a + b

def obtener_usuario(user_id):
    import sqlite3
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()
    query = "SELECT * FROM usuarios WHERE id = " + str(user_id)
    cursor.execute(query)
    resultado = cursor.fetchone()
    conn.close()
    return resultado

def ejecutar_comando(cmd):
    import os
    os.system(cmd)
    return True

def calcular(expr):
    return eval(expr)
