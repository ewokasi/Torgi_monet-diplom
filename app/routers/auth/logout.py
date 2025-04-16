from fastapi import Depends, Response
from fastapi.responses import RedirectResponse

from globals import *
import deco

@deco.try_decorator
async def logout(response : Response):
    response = RedirectResponse("/", status_code= 302)
    manager.set_cookie(response, "")
    return response
