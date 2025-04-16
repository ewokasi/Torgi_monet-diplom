import re
from fastapi import Depends, Response
from fastapi.responses import RedirectResponse
import deco
from globals import tm_db   
from datetime import datetime
import asyncio
from utils import date_form
from ..clientsCRUD.embeded_get_client import get
from ..clientsCRUD import add
from ..idCRUD import get_c_id
from .check_mail import check_mail
from .check_username import check_username 
from .check_phone import check_phone
from smtp.send_verification_mail import send_verification_mail
import html  # Для экранирования HTML-символов

# Регулярные выражения для валидации
EMAIL_REGEX = r'^[a-zA-Z0-9._%±]+@[a-zA-Z0-9.-]+.[a-zA-Z]{2,}$'
PHONE_REGEX = r'^\+7(\s|%20)\(\d{3}\)(\s|%20)\d{3}-\d{2}-\d{2}$'
NICKNAME_REGEX = r'^[a-zA-Z0-9_-а-яА-ЯёЁ]{3,16}$'  # Альфа-цифровые символы, _ или - и русские буквы

@deco.try_decorator
async def register(phone_number: str, password: str, nickname: str = "", email: str = "", avito_url: str = ""):
    try:
        # Очистка и защита данных
        phone_number = phone_number.replace(' ', '+', 1).strip()
        email = html.escape(email.strip())[:32]  # Экранирование + ограничение длины
        nickname = html.escape(nickname.strip())[:16]  # Экранирование + ограничение длины
        avito_url = avito_url.strip()[:64]  # Ограничение длины

        # Проверка на соответствие регулярным выражениям
        if not re.match(EMAIL_REGEX, email):
            return {"success": False, "error": "Некорректный формат email"}
        
        if not re.match(NICKNAME_REGEX, nickname):
            return {"success": False, "error": "Некорректный формат юзернейма"}

        # Проверка на уникальность
        if not await check_mail(email) and not await check_phone(phone_number) and not await check_username(nickname):
            await add(phone_number, password, email, nickname, avito_url)
            await send_verification_mail(email)
            return {"success": True, "message": "Регистрация успешна"}
        else:
            return {"success": False, "error": "Эта почта, юзернейм или номер телефона уже зарегистрированы"}
    
    except Exception as e:
        print(f"Ошибка в register: {e}")
        return {"success": False, "error": "Внутренняя ошибка сервера"}
