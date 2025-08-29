import smtplib

server = smtplib.SMTP("sandbox.smtp.mailtrap.io", 587)
server.starttls()  # TLS handshake
server.login("38bbc343ff54b0", "d16ee24ee59a5c")
print("Connected successfully")
server.quit()
