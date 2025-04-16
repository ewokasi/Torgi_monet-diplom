from globals import *
from fastapi import FastAPI, Request
from fastapi import Depends, Response
from globals import manager
from ..clientsCRUD import is_admin


async def admin(request: Request, user = Depends(manager)):
    
    user_buf = dict(await user)
    if not await is_admin( user_buf["email"]):
        return templates.TemplateResponse("about.html", context= {"request": request})
    else:
        return templates.TemplateResponse("admin.html", context= {"request": request})
                

