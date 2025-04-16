from fastapi import APIRouter, HTTPException
from globals import tm_db
from fastapi import Depends, Response
from globals import manager
from ..clientsCRUD import is_admin

async def delete(a_id: int, user = Depends(manager)):
    try:
        
        user_buf = dict(await user)
        if not user_buf['email']:
            return {"success": False, "error": "Вы не авторизованы."}
        elif not await is_admin( user_buf["email"]):
            return {"success": False, "error": "Вы не авторизованы."}
        collection = tm_db['auctions']
        
        # Обновляем запись, добавляя поле `deleted`
        result = await collection.update_one(
            {"a_id": a_id},  # Поиск по `a_id`
            {"$set": {"deleted": True}}  # Помечаем как удалённую
        )
        
        # Проверяем, было ли обновление успешным
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail=f"Аукцион с ID {a_id} не найден или уже удалён.")
        
        return {"status": "success", "message": f"Аукцион с ID {a_id} помечен как удалённый."}
    
    except Exception as e:
        return {"status": "error", "message": str(e)}
