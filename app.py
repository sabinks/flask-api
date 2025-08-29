import os
from flask import Flask
from flask_mail import Mail
from config import DevelopmentConfig, ProductionConfig, TestingConfig
from extensions import db, migrate, jwt
from routes.auth import auth_bp
from routes.posts import posts_bp
from routes.users import users_bp
from routes.general import general_bp
from models import Role

app = Flask(__name__)
env = os.getenv("FLASK_ENV", "development")

if env == "production":
    app.config.from_object(ProductionConfig)
elif env == "testing":
    app.config.from_object(TestingConfig)
else:
    app.config.from_object(DevelopmentConfig)

mail = Mail(app)

db.init_app(app)

migrate.init_app(app, db)
jwt.init_app(app)

# mail.init_app(app)

# Register Blueprints
app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(posts_bp, url_prefix="/api")
app.register_blueprint(users_bp, url_prefix="/api")
app.register_blueprint(general_bp, url_prefix="/api")

if __name__ == "__main__":
    app.run(debug=True)
