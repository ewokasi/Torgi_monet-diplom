from globals import tm_db

async def get_a_id():
    collection = tm_db['id_counters']
    try:
        # Increment the a_id field by 1 and return the updated document
        updated_document = await collection.find_one_and_update(
            {},
            {'$inc': {'a_id': 1}},
            return_document=True  # This option returns the updated document
        )
        
        if updated_document:
            #print(updated_document)
            return updated_document["a_id"]
        else:
            print("Документ для обновления не найден.")
            return None
    
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return None
