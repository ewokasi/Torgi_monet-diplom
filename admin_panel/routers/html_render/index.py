from globals import *
from fastapi import FastAPI, Request

async def index(request: Request):
    return templates.TemplateResponse("index.html", context= {"request": request})
