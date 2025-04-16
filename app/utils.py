from datetime import datetime


def date_form(input_date: str):
    # Ожидаем формат "дд.мм.гггг чч:мм"
    try:
        # Разбиваем дату и время
        date_part, time_part = input_date.split()
        
        # Разделяем дату и время на составляющие
        day, month, year = map(int, date_part.split('.'))
        hour, minute = map(int, time_part.split(':'))
        
        # Создаем объект datetime
        date_object = datetime(year, month, day, hour, minute)
        
        # Преобразуем в ISO формат с временной зоной +03:00
        output_date = date_object.isoformat() + "+03:00"
        
        return output_date
    except Exception as e:
        print(f"Error: {e}")
        

import pytz

# Функция для обработки формата DD.MM.YYYY HH:MM
def admin_date_form(date_string, timezone="Europe/Moscow"):
    naive_datetime = datetime.strptime(date_string, "%d.%m.%Y %H:%M")
    tz = pytz.timezone(timezone)
    localized_datetime = tz.localize(naive_datetime)  # Локализуем с указанным часовым поясом
    return localized_datetime.isoformat()  # Преобразуем в ISO строку




if __name__ == "__main__":
    print(date_form('12.12.2000 9:30'))