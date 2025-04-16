from globals import *
from fastapi import FastAPI, Request
from datetime import datetime


async def get(a_id:int , Request:Request):
    try:
       
        collection = tm_db['auctions']
        auctions = await collection.find_one({"a_id":a_id},{"_id": 0})
        return auctions
    
    except Exception as e:
        print(e)
        return e


async def alt_auction(request: Request):
    # Получаем параметр a_id из строки запроса
    a_id = request.query_params.get("a_id")
    
    # Загружаем данные аукциона из базы данных
    auction_data = await get(int(a_id), request)
    #print(auction_data)


    # Формируем метаинформацию
    meta_info = {
        "title": f"{auction_data["short_name"]}",
        "description": auction_data["description"],
        "structured_data": {
            "@context": "https://schema.org",
            "@type": "Auction",
            "name": auction_data["short_name"],
            "startDate": auction_data["start_datetime"],
            "endDate": auction_data["end_datetime"],
            "price": auction_data["start_price"],
            "url": str(request.url)
        }
    }

    # Передача метаинформации в шаблон
    return templates.TemplateResponse("alt_auction.html", context={
        "request": request,
        "auction_data": auction_data,
        "meta_info": meta_info
    })
