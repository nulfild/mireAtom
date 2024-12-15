# Базовый образ с Python
FROM python:3.9.5-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы проекта в контейнер
COPY . .

RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Устанавливаем переменную окружения для Flask
ENV FLASK_APP=run.py
ENV FLASK_ENV=production

# Открываем порт 5000
EXPOSE 5000

# Команда запуска приложения
CMD ["flask", "run", "--host=0.0.0.0"]
