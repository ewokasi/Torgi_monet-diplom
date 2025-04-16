from fastapi import APIRouter
from .robots import *
from .sitemap import *

ceo_router = APIRouter(
    prefix="",
    tags=["CEO"]
)

ceo_router.add_api_route(
    path='/robots.txt',
    endpoint=robots,
    methods=['GET']
)
ceo_router.add_api_route(
    path='/sitemap.xml',
    endpoint=sitemap,
    methods=['GET']
)