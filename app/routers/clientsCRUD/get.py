from globals import tm_db   
from datetime import datetime
import asyncio
from utils import date_form
from fastapi import Depends, Response
from globals import manager
from ..clientsCRUD import is_admin


async def get(clients_id: str, user = Depends(manager)):
    user_buf = dict(await user)
        
      
    if not user_buf['email']:
        return {"success": False, "error": "Вы не авторизованы."}
    elif not await is_admin( user_buf["email"]):
        return {"success": False, "error": "Вы не авторизованы."}
        
    try:
        collection = tm_db['clients']  # Исправлено название коллекции
        client = await collection.find_one({"id": int(clients_id)}, {"_id": 0})  # Исправлено поле поиска
        return client
    except Exception as e:
        print(e)
        return e