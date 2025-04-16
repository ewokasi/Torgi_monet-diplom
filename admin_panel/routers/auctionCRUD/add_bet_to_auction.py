from globals import tm_db   
from datetime import datetime, timedelta, timezone
from .get import get  
from .get_highest_bet import get_highest_bet
from .autoset_active_status import autoset_active_status  
from fastapi import Depends, Response
from smtp.mail_templates import target_bet_beated
from deco import try_decorator
from globals import tm_db   
from datetime import datetime
import asyncio
from utils import date_form
from globals import manager
from ..clientsCRUD import is_admin
from ..clientsCRUD.embeded_get_client import get as c_get

@try_decorator
async def add_bet_to_auction(a_id: str, bet_cost: int, user = Depends(manager)):
    try:
        user_buf = dict(await user)
        if not user_buf['phone_number']:   
            return {"success": False,"error": "Вы не авторизованы."}

        
        a_id = int(a_id)
        clients_id = int(user_buf['id'])
        await autoset_active_status(a_id)
        collection = tm_db['auctions']
        # Проверка существования аукциона
        auction = await collection.find_one({'a_id': a_id})
        if not auction:
            return {
                "status": "error",
                "message": "Аукцион не найден."
            }

        # Проверка активности аукциона
        if auction["is_active"] in [0, False]:
            return {
                "status": "error",
                "message": "Аукцион неактивен."
            }
       
        # Проверка существования клиента
        user = await c_get(clients_id) 
        if user == None:
            return {
                "status": "error",
                "message": "Клиент не найден."
            }

        if bet_cost<int(auction['start_price']):
            return {
                "status": "error",
                "message": f"Ставка должна быть больше, чем {str(auction['start_price'])}. Пожалуйста, сделайте новую ставку."
                
            }
      
        # Проверка на ставку больше последней
        last_bet = auction['bets'][-1] if auction['bets'] else None
        if last_bet and bet_cost < int(last_bet['bet_cost'])+int(auction["min_bid_step"]):
            return {
                "status": "error",
                "message": f"Ставка должна быть больше последней ставки {last_bet['bet_cost']} не менее чем на {str(auction['min_bid_step'])}. Пожалуйста, сделайте новую ставку."
                
            }
            
        if last_bet and bet_cost > (int(last_bet['bet_cost'])+int(auction["min_bid_step"]))*1.3:
            return {
                "status": "error",
                "message": f"Ставка должна быть не больше {(int(last_bet['bet_cost'])+int(auction["min_bid_step"]))*1.3}. Пожалуйста, сделайте новую ставку."
                
            }
            
        highest_bet = await get_highest_bet(a_id)
        # Добавление новой ставки
        bet_info = {
            "bet_cost": bet_cost,
            "clients_id": clients_id,
            "nickname": user['nickname'],
            "created_at": datetime.now(timezone.utc)
        }
        
        # Преобразуем строку даты с временной зоной в объект datetime
        end_datetime = datetime.fromisoformat(auction["end_datetime"])
        # Создаём offset-aware datetime для overtime_trigger
        overtime_trigger = datetime.now(timezone.utc) + timedelta(minutes=5)

        # Преобразуем overtime_trigger к временной зоне end_datetime, чтобы сравнить корректно
        overtime_trigger = overtime_trigger.astimezone(end_datetime.tzinfo)

        # Сравниваем даты и обновляем, если триггерное время больше
        if overtime_trigger > end_datetime:
            await collection.update_one(
                {'a_id': a_id},
                {'$set': {'end_datetime': str(overtime_trigger)}}
            )
        result = await collection.update_one(
            {'a_id': a_id},
            {'$push': {'bets': bet_info}}
        )
        
        if highest_bet:
            print("highest_bet ",highest_bet)
            await target_bet_beated(highest_bet['clients_id'])
        return {
            "status": "success",
            "message": "Ставка успешно добавлена."
        }

    except Exception as e:
        print(f"Error while adding bet: {e}")
        return {
            "status": "error",
            "message": f"Exception type: {type(e).__name__}, details: {str(e)}"
        }
