import subprocess

def ejecutar_query(query):
    import sqlite3
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    conn.close()
    return data

def backup_db(nombre_archivo):
    subprocess.call('tar -czf ' + nombre_archivo + '.tar.gz app.db', shell=True)
    subprocess.call('cp ' + nombre_archivo + '.tar.gz /backups/', shell=True)
    subprocess.call('echo Backup creado: ' + nombre_archivo, shell=True)

def importar_datos(ruta):
    f = open(ruta, 'r')
    contenido = f.read()
    for linea in contenido.split('\n'):
        campos = linea.split(',')
        query = "INSERT INTO datos VALUES ('" + campos[0] + "', '" + campos[1] + "')"
        ejecutar_query(query)
