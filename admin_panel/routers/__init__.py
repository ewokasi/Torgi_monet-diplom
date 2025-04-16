#тут мы импортируем все роутеры уровня ниже, чтобы
#потом не надо было добавлять много импортов в мейн
from .html_render.router import render_router
from .auctionCRUD.router import auction_router
from .clientsCRUD.router import clients_router
from .auth.router import auth_router
from .CEO.router import ceo_router