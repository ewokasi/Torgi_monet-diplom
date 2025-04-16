from globals import tm_db   

async def get(clients_id: str):
        
    try:
        collection = tm_db['clients']  # Исправлено название коллекции
        client = await collection.find_one({"id": int(clients_id)}, {"_id": 0})  # Исправлено поле поиска
        return client
    except Exception as e:
        print(e)
        return e
