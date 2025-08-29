import sys
import os

# Add the parent directory to the system path
# os.path.dirname(__file__) gets the current directory
# os.path.dirname(...) gets the parent directory
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import secrets

def current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# Many-to-many: User <-> Role
user_roles = db.Table("user_roles",
                      db.Column("user_id", db.Integer, db.ForeignKey("users.id")),  # fixed
                      db.Column("role_id", db.Integer, db.ForeignKey("roles.id"))  # fixed
                      )

role_permissions = db.Table(
    "role_permissions",
    db.Column("role_id", db.Integer, db.ForeignKey("roles.id"), primary_key=True),
    db.Column("permission_id", db.Integer, db.ForeignKey("permissions.id"), primary_key=True)
)


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    active = db.Column(db.Boolean, default=False, nullable=False)
    email_verified_at = db.Column(db.String(50), default=None, nullable=True)
    verification_token = db.Column(db.String(120), unique=True, nullable=True)
    created_at = db.Column(db.String(50), default=current_time, nullable=True)
    updated_at = db.Column(db.String(50), default=current_time, onupdate=current_time, nullable=True)

    posts = db.relationship("Post", backref="author", lazy=True)

    roles = db.relationship("Role", secondary=user_roles, back_populates="users", lazy="dynamic")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_verification_token(self):
        self.verification_token = secrets.token_urlsafe(32)


class Role(db.Model):
    __tablename__ = "roles"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    created_at = db.Column(db.String(50), nullable=False)
    updated_at = db.Column(db.String(50), nullable=False)

    users = db.relationship("User", secondary=user_roles, back_populates="roles")
    permissions = db.relationship("Permission", secondary=role_permissions, back_populates="roles")

    def __init__(self, name):
        now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        self.name = name
        self.created_at = now
        self.updated_at = now


class Permission(db.Model):
    __tablename__ = "permissions"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    method = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.String(50), nullable=False)
    updated_at = db.Column(db.String(50), nullable=False)

    roles = db.relationship("Role", secondary=role_permissions, back_populates="permissions")

    def __init__(self, name, method):
        now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        self.name = name
        self.method = method
        self.created_at = now
        self.updated_at = now


class Post(db.Model):
    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    publish = db.Column(db.Boolean, default=False, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)  # fixed
    created_at = db.Column(db.String(50), nullable=False)
    updated_at = db.Column(db.String(50), nullable=False)
