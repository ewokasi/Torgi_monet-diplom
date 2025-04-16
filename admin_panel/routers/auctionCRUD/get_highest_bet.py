from globals import tm_db   
from datetime import datetime
import asyncio
from utils import date_form

async def get_highest_bet(a_id:int):
    try:
        collection = tm_db['auctions']
        auctions = await collection.find_one({"a_id":a_id},{"_id": 0})
        if auctions["bets"]!=[]:
            return auctions["bets"][-1]
        else:
            return 0
    except Exception as e:
        print(e)
        return e
