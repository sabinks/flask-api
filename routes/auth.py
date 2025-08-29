from flask import Flask, Blueprint, request,jsonify, current_app
from extensions import db
from models import User, Role
from flask_jwt_extended import create_access_token
import jwt  
import datetime
import os
from dotenv import load_dotenv

load_dotenv()

auth_bp = Blueprint("auth", __name__)
app = Flask(__name__)

@auth_bp.route("/signup", methods=["POST"])
def signup():
    from sendmail import send_verification_email
    data = request.json
    if User.query.filter_by(email=data["email"]).first():
        return {"msg": "Email already registered"}, 400
    role = Role.query.filter_by(name="Member").first()
    if not role:
        role = Role(name="Member")
        db.session.add(role)
        db.session.commit()

    user = User(name=data["name"], email=data["email"])
    user.generate_verification_token()
    user.set_password(data["password"])

    # Default role: "User"
    role = Role.query.filter_by(name="Member").first()
    if role:
        user.roles.append(role)

    db.session.add(user)
    db.session.commit()
    send_verification_email(user)
    return {"msg": "User created successfully"}, 201

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    user = User.query.filter_by(email=data["email"]).first()
    if not user or not user.email_verified_at:
        return {"msg": "Email not verified, check email"}, 401
    if not user or not user.check_password(data["password"]):
        return {"msg": "Invalid credentials"}, 401
    secret_key = current_app.config['SECRET_KEY']
    
    token = jwt.encode(
        {
            "sub": user.email,   # subject = user identifier
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # expires in 1h
        },
        secret_key,
        algorithm="HS256"
    )
    return {"access_token": token}, 200


@auth_bp.route("/me", methods=["GET"])
def get_user_info():
    auth_header = request.headers.get("Authorization")
    
    # Validate header
    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({"msg": "Missing or invalid token"}), 401
    
    parts = auth_header.split(" ")
    if len(parts) != 2 or not parts[1]:
        return jsonify({"msg": "Malformed authorization header"}), 401
    
    token = parts[1]
    secret_key = current_app.config['SECRET_KEY']
    
    try:
        # Decode token
        payload = jwt.decode(token, secret_key, algorithms=["HS256"])
        
        # Validate payload
        email = payload.get("sub")
        if not email:
            return jsonify({"msg": "Invalid token payload"}), 401
        
        # Get user
        user = User.query.filter_by(email=email).first()
        if not user:
            return jsonify({"msg": "User not found"}), 404
        
        # Return safe info
        return jsonify({
            "user": {
                "id": user.id,
                "email": user.email,
                "name": user.name
            }
        })

    except jwt.ExpiredSignatureError:
        return jsonify({"msg": "Token expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"msg": "Invalid token"}), 401