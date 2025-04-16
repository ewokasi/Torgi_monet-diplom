from typing import Union

from fastapi import FastAPI, Request, BackgroundTasks
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import asyncio
from routers import *
from smtp.router import smtp_router
from routers.auctionCRUD.updater import update_all
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.middleware import SlowAPIMiddleware
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address, default_limits=["100/minute"])
#app = FastAPI(docs_url="/docs", redoc_url=None)
app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)


app.mount(
    "/static",
    StaticFiles(directory='app/static'),
    name="static",
)

app.include_router(render_router)
app.include_router(auction_router)
app.include_router(clients_router)
app.include_router(auth_router)
app.include_router(smtp_router)
app.include_router(ceo_router)

# Фоновая задача для обновления аукционов каждые 10 секунд
async def auto_update_task():
    while True:
        await update_all()  # Выполнение функции обновления
        await asyncio.sleep(10)  # Ждем 10 секунд

@app.on_event("startup")
async def start_auto_update():
    """
    Запускаем задачу автообновления при старте приложения.
    """
    # Запускаем фоновую задачу при старте приложения
    asyncio.create_task(auto_update_task())  # Создаем зада