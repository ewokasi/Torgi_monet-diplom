from globals import tm_db   
from datetime import datetime
import asyncio
from utils import date_form
from fastapi import Depends, Response
from globals import manager
from ..clientsCRUD import is_admin
from ..clientsCRUD.embeded_get_client import get

async def ban(id: int, user = Depends(manager)):
    try:
        
        user_buf = dict(await user)
        
      
        if not user_buf['email']:
            return {"success": False, "error": "Вы не авторизованы."}
        elif not await is_admin( user_buf["email"]):
            return {"success": False, "error": "Вы не авторизованы."}
        
        # Проверяем, существует ли клиент с данным client_id
        
        client_id = user_buf['id']
        collection = tm_db['clients']  # Коллекция, в которой хранятся данные клиентов
        
        client_data = await get(client_id)
        if client_data is None:
            return {
                "status": "error",
                "message": f"Клиент с ID {client_id} не существует."
            }

        # Обновляем статус пользователя на "заблокирован"
        update_result = await collection.update_one(
            {"id": id},
            {"$set": {"status": "banned"}}
        )

        # Проверяем, был ли обновлен документ
        if update_result.modified_count == 0:
            return{"status":'failed', "detail":"Не удалось заблокировать пользователя"}

        return {"message": "Пользователь успешно заблокирован"}
    
    except Exception as e:
        return{"status":'failed', "detail":str(e)}
