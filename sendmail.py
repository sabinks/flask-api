import os
from flask import render_template
from flask_mail import Message
from app import mail

def send_verification_email(user):
    token = user.verification_token
    verify_link = f"{os.getenv('FRONTEND_URL')}/email-verification?token={token}"

    html_body = render_template("verify_email.html", name=user.name, verify_link=verify_link)

    text_body = f"Hi {user.name},\n\nPlease verify your email: {verify_link}\n\nThank you!"

    msg = Message(
        subject="Email Verification",
        recipients=[user.email],
        body=text_body,
        html=html_body,
        sender='noreply@yourdomain.com'
    )

    mail.send(msg)
