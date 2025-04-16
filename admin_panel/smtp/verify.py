from globals import tm_db
from datetime import datetime

tokens_db = tm_db['tokens']

async def verify_email(token: str):
    # Ищем токен в базе данных
    token_data = await tokens_db.find_one({"token": token})

    if not token_data or token_data["expire_at"] <= datetime.now():
        return {"status": 'failed', "message": "Неверный или истёкший токен."}
    
    user_email = token_data.get("email")

    # Удаляем все токены для этого email
    await tokens_db.delete_many({"email": user_email})

    # Обновляем статус пользователя, что его почта подтверждена
    clients_db = tm_db['clients']
    await clients_db.update_one({"email": user_email}, {"$set": {"email_verified": True}})
    
    return {"status": "success", "message": f"Электронная почта {user_email} успешно подтверждена!"}
