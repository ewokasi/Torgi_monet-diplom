# Используйте базовый образ Python
FROM python:3.12

# Установите переменную окружения PYTHONUNBUFFERED для предотвращения буферизации вывода
ENV PYTHONUNBUFFERED 1

# Установите рабочую директорию внутри контейнера
WORKDIR /app
COPY . /app
COPY requirements.txt .

RUN pip install -r requirements.txt

EXPOSE 80
EXPOSE 443

# Команда, которая будет запущена при запуске контейнера
CMD ["python3", "app"]
