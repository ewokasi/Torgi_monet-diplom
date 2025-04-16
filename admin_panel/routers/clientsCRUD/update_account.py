from globals import tm_db
from ..idCRUD import get_c_id
from .embeded_get_client import get
from fastapi import Depends, Response
from globals import manager

async def update(json:dict, user = Depends(manager),):
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
        if "phone_number" in json:
            update_fields["phone_number"] = json["phone_number"]
        if "avito_url" in "avito_url" :
            update_fields["avito_url"] = json["avito_url"]
        if "mail_receive_bet_beated" in json:
            update_fields["mail_receive_bet_beated"] = json["mail_receive_bet_beated"]
        if "mail_receive_auction_started" in json:
            update_fields["mail_receive_auction_started"] = json["mail_receive_auction_started"]

        # Если нет полей для обновления, возвращаем сообщение
        if not update_fields:
            return {
                "status": "error",
                 "message": "Не указаны поля для обновления."
            }

        # Выполняем обновление данных в MongoDB
        result = await collection.update_one(
            {"id": client_id},
            {"$set": update_fields}
        )

        # Проверяем, обновился ли документ
        if result.modified_count > 0:
            return {
                "success": 1,
                "message": f"Клиент с ID {client_id} успешно обновлён."
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
