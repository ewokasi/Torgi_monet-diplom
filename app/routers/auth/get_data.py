from fastapi import Depends

from globals import *
import deco

@deco.try_decorator
async def get_data(user = Depends(manager)):
    user_buf = dict(await user)
    return dict((i, user_buf[i]) for i in user_buf if i != 'password')
