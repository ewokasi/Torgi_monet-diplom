from .set_active_status import set_active_status
from globals import tm_db
from datetime import datetime, timezone
from smtp.mail_templates import target_won_auction, mass_auction_started
from deco import try_decorator
async def get(a_id:int):
    try:
       
        collection = tm_db['auctions']
        auctions = await collection.find_one({"a_id":a_id},{"_id": 0})
     
        
        return auctions
    
    except Exception as e:
        print(e)
        return e
    
@try_decorator
async def autoset_active_status(a_id: int):
    auction = await get(a_id=a_id)
    current_time = datetime.now(timezone.utc)

    start_datetime = datetime.fromisoformat(auction["start_datetime"])
    end_datetime = datetime.fromisoformat(auction["end_datetime"])

    if start_datetime.tzinfo is None:
        start_datetime = start_datetime.replace(tzinfo=timezone.utc)
    if end_datetime.tzinfo is None:
        end_datetime = end_datetime.replace(tzinfo=timezone.utc)

    current_status = auction.get("is_active", 0)  # Default to 0 (inactive) if not found

    if start_datetime <= current_time < end_datetime:
        if current_status == 1:
            return  # No need to update status if it's already active
        # Trigger actions for starting the auction
        #await mass_auction_started(auction["short_name"], url=f'https://torgi.monety.shop/alt_auction?a_id={str(a_id)}')
        await set_active_status(a_id, 1)  # Set auction as active
    else:
        # If the auction has ended and status is not inactive, perform actions
        if current_status == 0:
            return  # No need to update status if it's already inactive
        # Perform actions for auction end
        #await target_won_auction(a_id)
        await set_active_status(a_id, 0)  # Set auction as inactive
