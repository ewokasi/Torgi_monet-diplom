from globals import *
from fastapi import FastAPI, Request

async def sidebar(request: Request):
    return templates.TemplateResponse("sidebar.html", context= {"request": request})
