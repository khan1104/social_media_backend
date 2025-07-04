
# import secure_smtplib 
import smtplib  
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import secrets
import os
from dotenv import load_dotenv
load_dotenv()

def generate_otp(length=6):
    """Generate a secure OTP."""
    return ''.join(secrets.choice('0123456789') for _ in range(length))

def send_email(to_email: str):
    sender_email = os.getenv("SENDER_EMAIL")
    password = os.getenv("APP_PASSWORD")  
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    subject="Otp code from talk for verification"
    otp=generate_otp()
    body=f'Hello, your OTP code is {otp}.'

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = to_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    context = ssl.create_default_context()
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)  
        server.starttls(context=context)
        server.login(sender_email, password)
        server.sendmail(sender_email, to_email, message.as_string())
        server.quit()
        print("✅ Email sent successfully to", to_email)
    except Exception as e:
        print("❌ Failed to send email:", e)

    return otp
