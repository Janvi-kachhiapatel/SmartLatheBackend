import smtplib

from email.mime.text import MIMEText


def send_otp(
    receiver_email,
    otp,
):

    sender_email = "smartlathe.iot@gmail.com"

    app_password = "YOUR_APP_PASSWORD"

    message = MIMEText(
        f"Your OTP is {otp}"
    )

    message["Subject"] = (
        "Smart Lathe Verification"
    )

    message["From"] = sender_email

    message["To"] = receiver_email

    server = smtplib.SMTP(
        "smtp.gmail.com",
        587
    )

    server.starttls()

    server.login(
        sender_email,
        app_password
    )

    server.sendmail(
        sender_email,
        receiver_email,
        message.as_string()
    )

    server.quit()