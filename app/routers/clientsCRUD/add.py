
from globals import tm_db   
from datetime import datetime
import asyncio
from utils import date_form
from .embeded_get_client import get
from ..idCRUD import get_c_id
from hashlib import sha256
import os



async def add(phone_number: str, password: str, email: str, nickname: str, avito_url: str = ""):
    try:
        clients_id = await get_c_id()
        if await get(clients_id)==None:

                        
            key = sha256(password.encode('utf-8')).hexdigest()
            
          
            insertion_c = {
                "id": clients_id,
                "phone_number": str(phone_number),
                "password": key,
                "email": email.lower().strip(),
                "avito_url": avito_url,
                "nickname": nickname.strip(),
                "mail_receive_bet_beated": True,
                "mail_receive_auction_started": True,
                "get_mails": True,
                'email_verified': False
            }
            collection = tm_db['clients']  # Исправлено название коллекции

            result = await collection.insert_one(insertion_c, bypass_document_validation=True)
            return {
                "status": "success",
                "message": f"Клиент с ID {clients_id} успешно добавлен."
            }
        else:
            return {
                    "status": "error",
                     "message": f"Клиент с ID {clients_id} уже существует."
                }
    except Exception as e:
        print(e)
        return e


