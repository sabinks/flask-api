from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from models import Post, User
from middleware import role_required

posts_bp = Blueprint("posts", __name__)

@posts_bp.route("/posts", methods=["POST"])
@jwt_required()
def create_post():
    user_id = get_jwt_identity()
    data = request.json
    post = Post(title=data["title"], content=data["content"], user_id=user_id)
    db.session.add(post)
    db.session.commit()
    return {"msg": "Post created"}, 201

@posts_bp.route("/posts", methods=["GET"])
@jwt_required()
def list_posts():
    posts = Post.query.all()
    return [{"id": p.id, "title": p.title, "author": p.author.username} for p in posts]

@posts_bp.route("/admin/posts", methods=["DELETE"])
@role_required("Admin")
def delete_all_posts():
    Post.query.delete()
    db.session.commit()
    return {"msg": "All posts deleted by Admin"}
