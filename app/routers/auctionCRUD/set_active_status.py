from globals import tm_db 

async def set_active_status(a_id: str, status: bool):
    collection = tm_db['auctions']
    
    # Обновляем документ с указанным a_id
    result = await collection.update_one(
        {'a_id': a_id},
        {'$set': {'is_active': status}}
    )
    
    # Проверяем, было ли обновлено что-то
    if result.modified_count > 0:
        return(f"Статус аукциона с ID {a_id} успешно обновлен на {status}.")
    else:
        return(f"Не удалось обновить статус аукциона с ID {a_id}. Возможно, он не существует.")
