from fastapi import APIRouter
from .verify import *
smtp_router = APIRouter(
    prefix="/mailservice",
    tags=["SMTP"]
)

smtp_router.add_api_route(
    path='/verify',
    endpoint=verify_email,
    methods=['GET']
)

