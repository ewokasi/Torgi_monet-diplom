from fastapi import APIRouter
from .index import *
from .account import *
from .alt_auction import *
from .create_auction import *
from .enter_reg_page import *
from .about import *
from .admin import *
from .sidebar import *

render_router = APIRouter(
    prefix="",
    tags=["Render"]
)

render_router.add_api_route(
    path='/',
    endpoint=index,
    methods=['GET']
)

render_router.add_api_route(
    path='/account',
    endpoint=account,
    methods=['GET']
)

render_router.add_api_route(
    path='/alt_auction',
    endpoint=alt_auction,
    methods=['GET']
)

render_router.add_api_route(
    path='/create_auction',
    endpoint=create_auction,
    methods=['GET']
)

render_router.add_api_route(
    path='/login',
    endpoint=enter_reg_page,
    methods=['GET']
)

render_router.add_api_route(
    path='/about',
    endpoint=about,
    methods=['GET']
)

render_router.add_api_route(
    path='/hello',
    endpoint=admin,
    methods=['GET']
)


render_router.add_api_route(
    path='/sidebar.html',
    endpoint=sidebar,
    methods=['GET']
)

