import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import random
import string
from mail_templates import send_mail


def generate_verification_token():
    """Генерация случайного токена для верификации (например, длиной 20 символов)"""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=20))

def send_verification_email(to_email, token):
    body = f"Пожалуйста, подтвердите вашу электронную почту, перейдя по следующей ссылке: {generate_verification_token()}"
    send_mail(to_email,"Подтвердите почту", body)
   



