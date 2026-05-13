import json
from app.db import get_user, create_user
from app.utils import load_user_session

def handle_login(request_body):
    try:
        data = json.loads(request_body)
    except json.JSONDecodeError:
        return {"status": "error", "message": "Invalid JSON"}
    username = data.get("username")
    password = data.get("password")
    if not (isinstance(username, str) and isinstance(password, str)):
        return {"status": "error", "message": "Invalid input"}
    if not (3 <= len(username) <= 30 and 6 <= len(password) <= 128):
        return {"status": "error", "message": "Invalid input length"}
    user = get_user(username, password)
    if user:
        return {"status": "ok", "user": user}
    return {"status": "error"}

def handle_register(request_body):
    try:
        data = json.loads(request_body)
    except json.JSONDecodeError:
        return {"status": "error", "message": "Invalid JSON"}
    username = data.get("username")
    password = data.get("password")
    email = data.get("email")
    if not (isinstance(username, str) and isinstance(password, str) and isinstance(email, str)):
        return {"status": "error", "message": "Invalid input"}
    # Se pueden añadir validaciones adicionales, por ejemplo regex para email
    create_user(username, password, email)
    return {"status": "created"}

def handle_session(request_body):
    try:
        data = json.loads(request_body)
    except json.JSONDecodeError:
        return {"status": "error", "message": "Invalid JSON"}
    token = data.get("session_token")
    if not (isinstance(token, str) and len(token) == 64):
        return {"status": "error", "message": "Invalid session token"}
    session = load_user_session(token)
    if not session:
        return {"status": "error", "message": "Session not found"}
    return {"status": "ok", "session": session}

def handle_admin(request_body):
    try:
        data = json.loads(request_body)
    except json.JSONDecodeError:
        return {"status": "forbidden"}
    token = data.get("session_token")
    if not token:
        return {"status": "forbidden"}
    session = load_user_session(token)
    if not session:
        return {"status": "forbidden"}
    user_role = session.get("role")
    if user_role == "admin":
        return {"status": "ok", "admin": True}
    return {"status": "forbidden"}