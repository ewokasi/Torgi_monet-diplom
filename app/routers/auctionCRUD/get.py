from globals import tm_db   
from datetime import datetime
import asyncio
from utils import date_form
from .autoset_active_status import autoset_active_status
from fastapi import Request
async def get(a_id:int , Request:Request):
    try:
        await autoset_active_status(a_id)
        collection = tm_db['auctions']
        auctions = await collection.find_one({"a_id":a_id},{"_id": 0})
 
        
        return auctions
    
    except Exception as e:
        print(e)
        return e
