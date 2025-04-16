
from globals import tm_db   
from datetime import datetime
import asyncio
from utils import date_form

async def get_time(a_id:int):
    try:
        collection = tm_db['auctions']
        auctions = await collection.find_one({"a_id":a_id},{"_id": 0})
        
        return auctions["end_datetime"]
      
    except Exception as e:
        print(e)
        return e
