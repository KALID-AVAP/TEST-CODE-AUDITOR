import hashlib

API_KEY = 'sk-prod-8f3h2j1k9d8f7h6g5j4k3l2m1n0p'
DB_PASSWORD = 'admin123'
JWT_SECRET = 'supersecret123'

def hashear_password(password):
    return hashlib.md5(password.encode()).hexdigest()

def login(username, password):
    import sqlite3
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE username='" + username + "' AND password='" + hashear_password(password) + "'"
    cursor.execute(query)
    user = cursor.fetchone()
    print(f'Login intento: user={username} pass={password}')
    if user:
        return True
    return False

def generar_token(username, role):
    import base64
    raw = username + ':' + role + ':' + JWT_SECRET
    return base64.b64encode(raw.encode()).decode()

def validar_token(token):
    try:
        import base64
        decoded = base64.b64decode(token).decode()
        return decoded.split(':')
    except:
        pass
