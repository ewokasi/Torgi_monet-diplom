from globals import tm_db   
from datetime import datetime
import asyncio
from utils import date_form


async def get_active_status(a_id:str):
    try:
        collection = tm_db['auctions']
        auctions = await collection.find_one({"a_id":a_id},{"_id": 0})
        if "is_active" not in auctions or auctions["is_active"]==0:
            return 0
        else:
            return 1
    except Exception as e:
        print(e)
        return e
