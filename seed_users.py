from werkzeug.security import generate_password_hash
from models import User, Role, user_roles, current_time  # adjust import if needed
from datetime import datetime
from extensions import db
from app import app
def seed_users():
    # Check if role already exists
    admin_role = Role.query.filter_by(name="admin").first()
    if not admin_role:
        admin_role = Role(name="admin")
        db.session.add(admin_role)
        db.session.commit()

    # Check if admin user exists
    admin_user = User.query.filter_by(email="admin@mail.com").first()
    if not admin_user:
        admin_user = User(
            name="Admin",
            email="admin@mail.com",
            password_hash=generate_password_hash("P@ss1234"),
            active=True,
            email_verified_at=current_time(),
            verification_token=None
        )
        db.session.add(admin_user)
        db.session.commit()

    # Assign role if not already assigned
    if admin_role not in admin_user.roles:
        admin_user.roles.append(admin_role)
        db.session.commit()

    print("✅ Admin user with role seeded successfully!")



if __name__ == "__main__":
    # app = create_app()
    with app.app_context():
        seed_users()
