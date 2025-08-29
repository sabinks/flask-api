from flask import Flask
from models import Role
from extensions import db
from app import app

def seed_roles():
    permissions = [
        {"name": "Admin"},
        {"name": "Member"},
    ]
    for perm in permissions:
        existing = Role.query.filter_by(name=perm["name"]).first()
        if not existing:
            new_perm = Role(
                name=perm["name"]
            )
            db.session.add(new_perm)

    db.session.commit()
    print("✅ Roles seeded!")

if __name__ == "__main__":
    # app = create_app()
    with app.app_context():
        seed_roles()
