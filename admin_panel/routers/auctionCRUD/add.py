from globals import tm_db   
from datetime import datetime, timezone
import asyncio
from utils import date_form
from .autoset_active_status import autoset_active_status
from .get import get
from ..idCRUD import get_a_id
from fastapi import Depends, Response
from globals import manager
from ..clientsCRUD import is_admin
from PIL import Image
import base64
from io import BytesIO

async def add( json: dict, user = Depends(manager)):
    try:
        #print(json)
        user_buf = dict(await user)
        if not user_buf['email']:
            return {"success": False, "error": "Вы не авторизованы. "}
        elif not await is_admin( user_buf["email"]):
            return {"success": False, "error": "Вы не авторизованы. "}
            
        
        
        a_id =await get_a_id()
        insertion = {
            "a_id": a_id,
            "short_name": json["short_name"].strip(), 
            "start_datetime": date_form(json["start_datetime"]), 
            "end_datetime": date_form(json["end_datetime"]), 
            "start_price": json["start_price"], 
            "min_bid_step": json["min_bid_step"],
            "description": json["description"],
            "bank": json["bank"],
            "bets": [],
            "created_at": datetime.now(timezone.utc),  
            "is_active": False
            
        }
        if insertion['start_datetime']==None: return {"status": "error",
            "message": f"Неправильно распознана дата начала"}
        if insertion['end_datetime']==None: return {"status": "error",
            "message": f"Неправильно распознана дата конца"}
            
        if "photo" in json:
            b64_string = json["photo"]
            
            # Декодируем Base64 в байты.
            image_data = base64.b64decode(b64_string)
            image = Image.open(BytesIO(image_data))

            # Определяем целевую высоту.
            target_height = 500

            # Рассчитываем новую ширину с сохранением пропорций.
            aspect_ratio = image.width / image.height
            target_width = int(target_height * aspect_ratio)

            # Изменяем размер изображения.
            resized_image = image.resize((target_width, target_height), Image.Resampling.LANCZOS)

            # Сохраняем обработанное изображение в строку Base64 (или в файл).
            output_buffer = BytesIO()
            resized_image.save(output_buffer, format=image.format)
            resized_b64 = base64.b64encode(output_buffer.getvalue()).decode('utf-8')

            # Обновляем запись.
            insertion["photo"] = resized_b64
        if "album" in json:
            insertion["album"]=json["album"]
            
        
        collection = tm_db['auctions']

        await collection.insert_one(insertion, bypass_document_validation=True)
        status_message = await autoset_active_status(a_id)

        return {
            "status": "success",
            "message": f"Аукцион с ID {a_id} успешно добавлен.",
            "autoset_status": status_message,
            "a_id":a_id
        }


    except Exception as e:
        print(f"Ошибка при добавлении аукциона: {e}")
        return {
            "status": "error",
            "message": str(e)
        }
