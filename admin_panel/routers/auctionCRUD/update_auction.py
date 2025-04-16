from fastapi import Depends, Response, Request, HTTPException
from globals import tm_db
from ..idCRUD import get_a_id
from .get import get
from globals import manager
import json as JSON
from datetime import datetime
from utils import admin_date_form as date_form
import pytz 
import base64
from io import BytesIO
from PIL import Image

async def update_auction(json: dict, Request: Request, user=Depends(manager)):
    try:
        # Проверяем, что пользователь аутентифицирован
        user_buf = dict(await user)
        client_id = user_buf.get('id')
        if not client_id:
            raise HTTPException(status_code=401, detail="Пользователь не авторизован.")

        # Получаем коллекцию аукционов
        collection = tm_db['auctions']

        # Проверяем, передан ли a_id
        auction_id = json.get("a_id")
        if not auction_id or not isinstance(auction_id, str):
            return {
                "success": 0,
                "message": "Некорректный или отсутствующий ID аукциона."
            }  

        # Проверяем, существует ли аукцион с данным a_id
        auction_data = await get(int(auction_id), Request)
        if auction_data is None:
            return {
                "success": 0,
                "message": f"Аукцион с ID {auction_id} не существует."
            }

        # Формируем словарь для обновления только с валидными полями
        update_fields = {}

        if "short_name" in json:
            short_name = json["short_name"]
            if isinstance(short_name, str) and short_name.strip():
                update_fields["short_name"] = short_name.strip()

                
        if "start_datetime" in json:
            start_datetime = json["start_datetime"]
            try:
                # Пытаемся сначала распарсить ISO формат
                iso_datetime = datetime.fromisoformat(start_datetime)
                if iso_datetime.tzinfo is None:  # Если часовой пояс не указан
                    tz = pytz.timezone("Europe/Moscow")
                    iso_datetime = tz.localize(iso_datetime)
                update_fields["start_datetime"] = iso_datetime.isoformat()
            except ValueError:
                try:
                    # Если ISO не сработал, пытаемся распарсить формат DD.MM.YYYY HH:MM
                    update_fields["start_datetime"] = date_form(start_datetime)
                except ValueError:
                    return {
                        "success": 0,
                        "message": "Некорректный формат start_datetime. Ожидается ISO формат или DD.MM.YYYY HH:MM."
                    }

        if "end_datetime" in json:
            end_datetime = json["end_datetime"]
            try:
                # Пытаемся сначала распарсить ISO формат
                iso_datetime = datetime.fromisoformat(end_datetime)
                if iso_datetime.tzinfo is None:  # Если часовой пояс не указан
                    tz = pytz.timezone("Europe/Moscow")
                    iso_datetime = tz.localize(iso_datetime)
                update_fields["end_datetime"] = iso_datetime.isoformat()
            except ValueError:
                try:
                    # Если ISO не сработал, пытаемся распарсить формат DD.MM.YYYY HH:MM
                    update_fields["end_datetime"] = date_form(end_datetime)
                except ValueError:
                    return {
                        "success": 0,
                        "message": "Некорректный формат end_datetime. Ожидается ISO формат или DD.MM.YYYY HH:MM."
                    }
        if "start_price" in json:
            start_price = int(json["start_price"])
            if isinstance(start_price, (int, float)) and start_price > 0:
                update_fields["start_price"] = start_price
            else:
                return {
                    "success": 0,
                    "message": "start_price должен быть положительным числом."
                }

        if "min_bid_step" in json:
            min_bid_step = int(json["min_bid_step"])
            if isinstance(min_bid_step, (int, float)) and min_bid_step > 0:
                update_fields["min_bid_step"] = min_bid_step
            else:
                return {
                    "success": 0,
                    "message": "min_bid_step должен быть положительным числом."
                }

        if "description" in json:
            description = json["description"]
            if isinstance(description, str) and description.strip():
                update_fields["description"] = description.strip()

        if "photo" in json:
            photo = json["photo"]
            if isinstance(photo, str) and photo.strip().startswith("data:image/"):
                # Убираем часть с "data:image/format;base64,"
                photo_data = photo.split(",", 1)[1]
                
                # Декодируем Base64 в байты.
                image_data = base64.b64decode(photo_data)
                image = Image.open(BytesIO(image_data))
                
                # Конвертируем изображение в RGB, чтобы отбросить альфа-канал.
                image = image.convert("RGB")

                # Сохраняем изображение в формате JPEG.
                output_buffer = BytesIO()
                image.save(output_buffer, format="JPEG", quality=85)  # Устанавливаем качество.
                
                # Кодируем результат обратно в Base64.
                jpeg_b64 = base64.b64encode(output_buffer.getvalue()).decode("utf-8")

                # Обновляем поле фото.
                update_fields["photo"] = f"{jpeg_b64}"
        if "bets" in json:
            try:
                bets = JSON.loads(json["bets"])
                if isinstance(bets, list):
                    update_fields["bets"] = bets
                else:
                    return {
                        "success": 0,
                        "message": "bets должен быть массивом."
                    }
            except JSON.JSONDecodeError:
                return {
                    "success": 0,
                    "message": "Некорректный формат bets. Ожидается JSON массив."
                }

        # Если нет полей для обновления, возвращаем сообщение
        if not update_fields:
            return {
                "success": 0,
                "message": "Не указаны поля для обновления."
            }

        # Выполняем обновление данных в MongoDB
        result = await collection.update_one(
            {"a_id": int(auction_id)},
            {"$set": update_fields}
        )

        # Проверяем, обновился ли документ
        if result.modified_count > 0:
            return {
                "success": 1,
                "message": f"Аукцион с ID {auction_id} успешно обновлён."
            }
        else:
            return {
                "success": 0,
                "message": f"Изменения для аукциона с ID {auction_id} не были внесены."
            }

    except Exception as e:
        # Логируем ошибку для дальнейшей отладки
        print(f"Ошибка: {e}")
        return {
            "success": 0,
            "message": f"Произошла ошибка: {str(e)}"
        }
