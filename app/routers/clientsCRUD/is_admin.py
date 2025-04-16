from globals import tm_db   
from datetime import datetime
import asyncio
from utils import date_form

async def is_admin(email: str):
    try:
        collection = tm_db['admins'] 
        client = await collection.find_one({"email": email}, {"_id": 0})  
        #print(client)
        if client!=None:
            return 1
    except Exception as e:
        print(e)
        return 0