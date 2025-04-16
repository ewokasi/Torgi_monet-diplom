from globals import tm_db   
from datetime import datetime
import asyncio
from utils import date_form

async def get_unique_mails(filter_key):
    try:
        collection = tm_db['clients']  # Подключаем коллекцию
        clients = await collection.find(
            {filter_key: True}, 
            {"_id": 0, "email": 1}  # Получаем только email
        ).to_list(length=None)
        
        unique_emails = set(client["email"] for client in clients if "email" in client)  # Убираем дубли
        return list(unique_emails)
    except Exception as e:
        print(e)
        return e

async def get_mails_to_notify():
    return await get_unique_mails("mail_receive")

async def get_mails_to_notify_start():
    return await get_unique_mails("mail_receive_auction_started")