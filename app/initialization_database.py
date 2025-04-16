from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi
from config import config


# Асинхронная функция для проверки и создания коллекций с определенной схемой
async def setup_collections(db: AsyncIOMotorClient):
    
    collections = await db.list_collection_names()
    if 'clients' not in collections:
        await db.create_collection('clients')
        print("Created clients collection")


    if 'auctions' not in collections:
        await db.create_collection('auctions')
        print("Created auctions collection")
    
    if 'tokens' not in collections:
        await db.create_collection('tokens')
        print("Created tokens collection")
        
        
    if 'admins' not in collections:
        await db.create_collection('admins')
        insertion = {
                    "email":'kostyakov0203@mail.ru'
                }
        db['admins'].insert_one(insertion)
                

    if 'id_counters' not in collections:
        await db.create_collection('id_counters')
        print("Created id_counters collection")
    
        insertion = {
            "a_id":0,
            "clients_id":1
        }
        db['id_counters'].insert_one(insertion)
        print("inserted init values for id_counter")

    return

