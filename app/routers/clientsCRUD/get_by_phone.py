from globals import tm_db   
from datetime import datetime
import asyncio
from utils import date_form

async def get_by_phone(phone: str):
    try:
        collection = tm_db['clients']  # Исправлено название коллекции
        client = await collection.find_one({"phone_number": phone}, {"_id": 0})  # Исправлено поле поиска
        return client
    except Exception as e:
        print(e)
        return e