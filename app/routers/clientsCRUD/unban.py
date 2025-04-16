from fastapi import Depends, HTTPException
from globals import tm_db, manager
from ..clientsCRUD.embeded_get_client import get
from ..clientsCRUD import is_admin

async def unban(id: int, user = Depends(manager)):
    try:
        # Получаем информацию о текущем пользователе
        user_buf = dict(await user)
        client_id = user_buf['email']

        # Проверяем, является ли пользователь администратором
        if not await is_admin(client_id):
            raise HTTPException(status_code=403, detail="У вас нет прав на разблокировку пользователей.")

        collection = tm_db['clients']  # Коллекция, в которой хранятся данные клиентов

        # Проверяем, существует ли клиент с данным id
        client_data = await get(id)
        if not client_data:
            raise HTTPException(status_code=404, detail=f"Клиент с ID {id} не найден.")

        # Обновляем статус пользователя, удаляя поле "status" (разбан)
        result = await collection.update_one(
            {"id": id},  # Используем id для поиска
            {"$unset": {"status": ""}}  # Удаляем поле "status", которое, вероятно, означает бан
        )

        if result.modified_count == 0:
            raise HTTPException(status_code=400, detail="Не удалось разблокировать пользователя или пользователь не был заблокирован.")

        return {"status": "success", "message": f"Пользователь с ID {id} был разблокирован."}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
