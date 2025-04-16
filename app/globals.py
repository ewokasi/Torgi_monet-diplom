from config import config
#все глобальные переменные

from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory="app/templates")


###################################################################
#MongoDB
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi
import asyncio
from initialization_database import setup_collections


db_client = AsyncIOMotorClient(config.get('MongoDB')["url"], server_api=ServerApi('1'))
tm_db = db_client['Torgi_Monet']  # Создаем или подключаемся к базе данных 'Monetochki'

async def ping_server():
  try:
      await db_client.admin.command('ping')
      print("Pinged your deployment. You successfully connected to MongoDB!")
      await setup_collections(tm_db)
  except Exception as e:
      print(e)

#asyncio.run(ping_server())

########################################################################

smtp_username = config.get('Smtp')["login"]
smtp_password = config.get('Smtp')["password"]
smtp_link = config.get('Smtp')["start_url"]

########################################################################
from fastapi_login import LoginManager

SECRET_KEY = "SECRET_KEY"

manager = LoginManager(
    SECRET_KEY,
    token_url='/auth/token',
    use_cookie=True,
    use_header=False
)


async def get_user(mail: str):
    try:
        collection = tm_db['clients']
        
        # Находим пользователя по email
        client = await collection.find_one({"email": mail}, {"_id": 0})
        
        # Проверяем, найден ли пользователь и не заблокирован ли он
        if client is None:
            return None
        
        if client.get("status") == "banned":
            return None
    
        return client  # Возвращаем данные пользователя, если он не заблокирован
        
    except Exception as e:
        print(e)
        return {"error": str(e)}

        
    except Exception as e:
        print(e)
        return {"error": str(e)}

@manager.user_loader()
def load_user(mail: str):
    user = get_user(mail.lower())
   
    return user
