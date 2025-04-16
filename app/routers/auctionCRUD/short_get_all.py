from globals import tm_db   
from datetime import datetime
import asyncio
from utils import date_form


async def short_get_all():
    try:
        collection = tm_db['auctions']
        auctions = await collection.find( {"deleted": {"$exists": False}},{"_id": 0,"a_id":1, "short_name":1}).to_list(length=None) 
        return auctions
    except Exception as e:
        print(e)
        return e
