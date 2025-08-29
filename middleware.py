from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from models import User

def role_required(*roles):
    """
    Usage: @role_required("Admin", "Editor")
    """
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()  # validate JWT
            user_id = get_jwt_identity()
            user = User.query.get(user_id)
            if not user:
                return {"msg": "User not found"}, 404
            
            user_roles = [role.name for role in user.roles]
            if not any(role in user_roles for role in roles):
                return {"msg": "Permission denied"}, 403
            
            return fn(*args, **kwargs)
        return wrapper
    return decorator
