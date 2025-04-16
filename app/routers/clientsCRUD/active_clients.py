from fastapi import APIRouter, Depends
from globals import tm_db
from collections import Counter
from globals import manager

async def active_clients(user=Depends(manager)):
    # Получаем коллекции
    auctions_collection = tm_db['auctions']
    clients_collection = tm_db['clients']

    # Получаем все аукционы и пользователей
    auctions = await auctions_collection.find().to_list(None)
    clients = await clients_collection.find().to_list(None)

    # Подсчитываем количество ставок каждого клиента
    bet_counter = Counter()
    for auction in auctions:
        for bet in auction.get("bets", []):
            client_id = bet.get("clients_id")
            if client_id is not None:
                bet_counter[client_id] += 1

    # Создаем список активных пользователей
    active_clients = []
    for client in clients:
        client_id = client.get("id")
        client_bets = bet_counter.get(client_id, 0)  # Получаем количество ставок пользователя
        if client_bets > 0:
            active_clients.append({
                "id": client_id,
                "nickname": client.get("nickname"),
                "email": client.get("email"),
                "phone_number": client.get("phone_number"),
                "bet_count": client_bets
            })

    # Сортируем пользователей по количеству ставок (по убыванию)
    active_clients = sorted(active_clients, key=lambda x: x["bet_count"], reverse=True)

    return active_clients
