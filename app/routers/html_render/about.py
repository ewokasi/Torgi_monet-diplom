from globals import *
from fastapi import FastAPI, Request

async def about(request: Request):
    return templates.TemplateResponse("about.html", context= {"request": request})
