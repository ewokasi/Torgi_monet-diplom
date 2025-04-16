from fastapi import Depends, Response
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_login.exceptions import InvalidCredentialsException
from datetime import timedelta
from hashlib import sha256
import os
from globals import *
from smtp.send_verification_mail import send_verification_mail

async def login(response: Response, data: OAuth2PasswordRequestForm = Depends()):
    login = str(data.username)
    password = data.password
    key = sha256(password.encode('utf-8')).hexdigest()
    password = key

    user = await load_user(login)
    if not user:
        raise InvalidCredentialsException
    elif user['email_verified']==False:
        await send_verification_mail(user["email"])
        return "Ваша почта не подтверждена, сообщение отправлено на почту"
    elif password != user['password']:
        raise InvalidCredentialsException
    

    access_token = manager.create_access_token(
        data=dict(sub=login), expires = timedelta(hours = 720)
    )
    manager.set_cookie(response, access_token)

    return {'access_token': access_token, 'token_type': 'bearer'}
