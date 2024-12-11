from flask import Flask
from dotenv import load_dotenv
import os

from app.db import db
from app.routes import init_routes

# Загружаем переменные окружения
load_dotenv()

DB_USERNAME = os.getenv('DB_USERNAME', 'postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'postgres')
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', 5432)
DB_DATABESE = os.getenv('DB_DATABESE', 'FormulDB')
PORT = os.getenv('PORT', 5010)

def create_app():
    """
    Создаёт и возвращает экземпляр Flask-приложения.
    """
    app = Flask(__name__)

    # Настройки приложения
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABESE}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Инициализация расширений
    db.init_app(app)

    # Регистрация маршрутов
    init_routes(app)

    return app
