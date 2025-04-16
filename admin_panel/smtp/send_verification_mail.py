from .mail_templates import send_mail
import random
import aiosmtplib
import string
from globals import tm_db
from globals import smtp_link
from datetime import timedelta, datetime

def generate_verification_token(target:str):
    """Генерация случайного токена для верификации (например, длиной 20 символов)"""
    token =''.join(random.choices(string.ascii_letters + string.digits, k=20))
    collection = tm_db['tokens'] 
    collection.insert_one({"email":target, "token": token, "expire_at": datetime.now() + timedelta(hours=24) })  

    return token

async def send_verification_mail(target:str):
    token = generate_verification_token(target)
    verification_link = f"{smtp_link}/mailservice/verify?token={token}"

    body = "Чтобы подтвердить свою почту перейдите по ссылке\n"+verification_link
    await send_mail(target, "Подтверждение почты", body)