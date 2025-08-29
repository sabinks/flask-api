from flask import Flask
from models import Permission
from extensions import db
from app import app
def seed_permissions():
    permissions = [
        {"name": "view_posts", "method": "get"},
        {"name": "store_post", "method": "post"},
        {"name": "show_post", "method": "get"},
        {"name": "update_post", "method": "post"},
        {"name": "delete_post", "method": "delete"},
    ]
    for perm in permissions:
        existing = Permission.query.filter_by(name=perm["name"]).first()
        if not existing:
            new_perm = Permission(
                name=perm["name"],
                method=perm["method"]
            )
            db.session.add(new_perm)

    db.session.commit()
    print("✅ Permissions seeded!")

if __name__ == "__main__":
    # app = create_app()
    with app.app_context():
        seed_permissions()
