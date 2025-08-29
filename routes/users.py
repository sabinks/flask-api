from flask import Blueprint
from flask_jwt_extended import jwt_required
from models import User
from middleware import role_required

users_bp = Blueprint("users", __name__)

@users_bp.route("/users", methods=["GET"])
@role_required("Admin")

def get_users():
    users = User.query.all()
    return [{"id": u.id, "name": u.name, "roles": [r.name for r in u.roles]} for u in users]
