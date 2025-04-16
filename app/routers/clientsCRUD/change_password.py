from globals import tm_db
from ..idCRUD import get_c_id
from .embeded_get_client import get
from fastapi import Depends, Response
from globals import manager
from hashlib import sha256
from ..auth import logout

async def change_password(json:dict, user = Depends(manager),):
    try:
        
        user_buf = dict(await user)
        client_id = user_buf['id']
        collection = tm_db['clients']  # Коллекция, в которой хранятся данные клиентов

        # Проверяем, существует ли клиент с данным client_id
        client_data = await get(client_id)
        if client_data is None:
            return {
                "status": "error",
                "message": f"Клиент с ID {client_id} не существует."
            }

        # Формируем словарь для обновления только с теми полями, которые были переданы
        update_fields = {}
        
        key = sha256(json["old_password"].encode('utf-8')).hexdigest()

        if key ==client_data["password"]:
            result = await collection.update_one(
            {"id": client_id},
            {"$set": {"password":sha256(json["new_password"].encode('utf-8')).hexdigest()}}
        )

       

        # Выполняем обновление данных в MongoDB
      

        # Проверяем, обновился ли документ
        if result.modified_count > 0:
          
            return {
                    "success": 1,
                    "message": f""
                }
        else:
            return {
                "success": 0,
                "message": f"Изменения для клиента с ID {client_id} не были внесены."
            }

    except Exception as e:
        print(e)
        return {
            "success": 0,
            "message": f"Произошла ошибка: {str(e)}"
        }
