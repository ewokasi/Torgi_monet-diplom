from globals import tm_db
from ..idCRUD import get_c_id
from .embeded_get_client import get
from fastapi import Depends, Response
from globals import manager
from .is_admin import is_admin

async def edit(json: dict, user=Depends(manager)):
    try:
        #print(json)
        user_buf = dict(await user)
        client_id = user_buf['id']
        
       
        collection = tm_db['clients']  # Коллекция, в которой хранятся данные клиентов
        
        # Проверяем, существует ли клиент с данным ID
        client_data = await get(json["id"])
        if client_data is None:
            return {
                "status": "error",
                "message": f"Клиент с ID {json['id']} не существует."
            }
        
        # Формируем словарь для обновления только с измененными полями
        update_fields = {}
        fields_to_check = [
            "phone_number",
            "nickname",
            "avito_url",
            "mail_receive_bet_beated",
            "mail_receive_auction_started"
        ]
        for field in fields_to_check:
            if field in json and json[field] != client_data.get(field):
                # Проверяем и преобразуем строковые значения "True" / "False" в булевы
                if isinstance(json[field], str) and json[field].lower() in ["true", "false"]:
                    update_fields[field] = json[field].lower() == "true"
                else:
                    update_fields[field] = json[field]

        
        # Если нет полей для обновления, возвращаем сообщение
        if not update_fields:
            return {
                "status": "error",
                "message": "Не указаны поля для обновления или изменения совпадают с текущими."
            }
        
        # Выполняем обновление данных в MongoDB
        result = await collection.update_one(
            {"id": int(json["id"])},  # Используем ID из переданного JSON
            {"$set": update_fields}
        )
        
        # Проверяем, обновился ли документ
        if result.modified_count > 0:
            return {
                "success": 1,
                "message": f"Клиент с ID {json['id']} успешно обновлён."
            }
        else:
            return {
                "success": 0,
                "message": f"Изменения для клиента с ID {json['id']} не были внесены."
            }
    
    except Exception as e:
        print(e)
        return {
            "success": 0,
            "message": f"Произошла ошибка: {str(e)}"
        }
