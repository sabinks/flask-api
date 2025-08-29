from flask import Blueprint, request, jsonify
from extensions import db
from models import User
from models import current_time

general_bp = Blueprint("general", __name__)

@general_bp.route("/verify-email", methods=["POST"])
def verify_email():
    token = request.args.get("token")
    user = User.query.filter_by(verification_token=token).first()
    if user:
        user.email_verified_at = current_time()
        user.verification_token = None
        user.active = True
        db.session.commit()

        return jsonify({"message": "Email verified successfully"})
    return jsonify({"message": "Invalid or expired token"}), 400