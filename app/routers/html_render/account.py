from globals import *
from fastapi import FastAPI, Request

async def account(request: Request):
    return templates.TemplateResponse("account.html", context= {"request": request})