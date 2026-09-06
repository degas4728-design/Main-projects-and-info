from functools import wraps
from flask import request, jsonify
from di.container import Container

def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")
        user_id = Container().get_auth_service().authenticate(auth_header)
        if not user_id:
            return jsonify({"error": "Требуется авторизация"}), 401
        kwargs["current_user_id"] = user_id
        return f(*args, **kwargs)
    return decorated