from globals import tm_db   
from datetime import datetime
import asyncio
from utils import date_form

async def check_mail(mail: str):
    try:
        collection = tm_db['clients']  # Исправлено название коллекции
        client = await collection.find_one({"email": mail}, {"_id": 0})  # Исправлено поле поиска
        
        if client:
            return 1
        else: 
            return 0
    except Exception as e:
        print(e)
        return e