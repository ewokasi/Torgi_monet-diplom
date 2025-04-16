from functools import wraps
import os
import sys
from globals import *

def try_decorator(func):
    @wraps(func)
    async def inner_function(*args, **kwargs):
        try:
            return await func(*args, **kwargs)

        except Exception as e:
            function_name = func.__name__
           
            return {
                "error": {
                    "body": str(e),
                    "function": function_name
                },
                "success": False
            }
    return inner_function
