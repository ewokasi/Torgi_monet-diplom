from globals import *
from fastapi import FastAPI, Request

async def enter_reg_page(request: Request):
    return templates.TemplateResponse("enter_reg_page.html", context= {"request": request})
