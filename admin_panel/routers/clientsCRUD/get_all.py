from globals import tm_db   
from datetime import datetime
import asyncio
from utils import date_form
from fastapi import Depends, Response
from globals import manager
from .is_admin import is_admin

async def get_all(user = Depends(manager)):
    try:
        user_buf = dict(await user)
        
      
        if not user_buf['email']:
            return {"success": False, "error": "Вы не авторизованы."}
        elif not await is_admin( user_buf["email"]):
            return {"success": False, "error": "Вы не авторизованы."}
        
        collection = tm_db['clients']  # Исправлено название коллекции
        clients = await collection.find({}, {"_id": 0}).to_list()
        return clients
    except Exception as e:
        print(e)
        return e
