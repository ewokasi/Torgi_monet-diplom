from fastapi import APIRouter
from .add import *
from .get_all import *
from .get import *
from .update_account import * 
from .change_password import * 
from .active_clients import * 
from .ban import * 
from .unban import * 
from .edit_account import edit

clients_router = APIRouter(
    prefix="/mongo/clients",
    tags=["API"]
)

clients_router.add_api_route(
    path='/add',
    endpoint=add,
    methods=['POST']
)
clients_router.add_api_route(
    path='/get_all',
    endpoint=get_all,
    methods=['GET']
)
clients_router.add_api_route(
    path='/get',
    endpoint=get,
    methods=['GET']
)

clients_router.add_api_route(
    path='/update',
    endpoint=update,
    methods=['POST']
)

clients_router.add_api_route(
    path='/change_password',
    endpoint=change_password,
    methods=['POST']
)

clients_router.add_api_route(
    path='/active_clients',
    endpoint=active_clients,
    methods=['POST']
)


clients_router.add_api_route(
    path='/ban',
    endpoint=ban,
    methods=['DELETE']
)

clients_router.add_api_route(
    path='/unban',
    endpoint=unban,
    methods=['POST']
)


clients_router.add_api_route(
    path='/edit',
    endpoint=edit,
    methods=['POST']
)

