from fastapi import APIRouter
from .add import *
from .get_all import *
from .get import *
from .add_bet_to_auction import *
from .short_get_all import *
from .update_auction import *
from .delete import *
from .get_bets import *
from .get_time import *


auction_router = APIRouter(
    prefix="/mongo/auction",
    tags=["Auctions"]
)

auction_router.add_api_route(
     path='/add',
    endpoint=add,
    methods=['POST']
)
auction_router.add_api_route(
     path='/add_bet_to_auction',
    endpoint=add_bet_to_auction,
    methods=['POST']
)

auction_router.add_api_route(
     path='/get_all',
    endpoint=get_all,
    methods=['GET']
)

auction_router.add_api_route(
     path='/get',
    endpoint=get,
    methods=['GET']
)


auction_router.add_api_route(
     path='/short_get_all',
    endpoint=short_get_all,
    methods=['GET']
)

auction_router.add_api_route(
     path='/update_auction',
    endpoint=update_auction,
    methods=['POST']
)



auction_router.add_api_route(
     path='/delete',
    endpoint=delete,
    methods=['DELETE']
)



auction_router.add_api_route(
     path='/get_bets',
    endpoint=get_bets,
    methods=['GET']
)

auction_router.add_api_route(
     path='/get_time',
    endpoint=get_time,
    methods=['GET']
)


