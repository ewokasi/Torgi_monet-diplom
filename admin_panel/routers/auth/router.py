from fastapi import APIRouter

from .login import login
from .get_data import get_data
from .logout import logout
from .register import register
from .check_mail import check_mail

auth_router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

auth_router.add_api_route(
    "/token",
    login,
    description="Авторизация (сюда логин и пароль)",
    methods=['POST']
)

auth_router.add_api_route(
    "/get_data",
    get_data,
    description="Получить информацию о пользователе",
    methods=['GET']
)

auth_router.add_api_route(
    "/logout",
    logout,
    description="Выйти из аккаунта",
    methods=['POST']
)

auth_router.add_api_route(
    "/register",
    register,
    description="Создать новый аккаунт",
    methods=['POST']
)
auth_router.add_api_route(
    "/check_mail",
    check_mail,
    description="",
    methods=['POST']
)
