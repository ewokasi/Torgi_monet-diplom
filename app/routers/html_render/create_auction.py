from globals import *
from fastapi import FastAPI, Request
from fastapi import Depends, Response
from globals import manager
from ..clientsCRUD import is_admin

async def create_auction(request: Request, user = Depends(manager)):
    user_buf = dict(await user)
    print(user_buf)
    if not await is_admin(user_buf["email"]):
        return {"success": False, "error": "Вы не авторизованы."}
    else:
        return templates.TemplateResponse("create_auction.html", context= {"request": request})
