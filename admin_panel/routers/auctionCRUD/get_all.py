from globals import tm_db   
from datetime import datetime
import asyncio
from utils import date_form
from .autoset_active_status import autoset_active_status

async def get_all():
    try:
        collection = tm_db['auctions']
        
        # Запрос только для документов, у которых нет поля `deleted`
        auctions = await collection.find(
            {"deleted": {"$exists": False}},  # Условие отсутствия поля `deleted`
            {"_id": 0, "album":0}  # Исключение поля `_id` из результата
        ).to_list(length=None)
        
        return auctions
    except Exception as e:
        print(e)
        return {"error": str(e)}  # Возвращаем сообщение об ошибке как строку для удобства
