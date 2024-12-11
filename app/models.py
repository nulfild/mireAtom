from datetime import datetime
from app.db import db

class Formula(db.Model):
    """
    Модель базы данных для формулы.

    Атрибуты:
        id (int): Уникальный идентификатор формулы.
        fullName (str): Название формулы.
        normalized (str): Нормализованная формула
        expression (str): Математическое выражение формулы.
        date (datetime): Дата создания формулы
    """
    __tablename__ = 'formulas'
    id = db.Column(db.Integer, primary_key=True)
    fullName = db.Column(db.String(100), nullable=False)
    normalized = db.Column(db.String(255), nullable=False)
    expression = db.Column(db.String(255), nullable=False)
    date = db.Column(db.DateTime, nullable = False, default = datetime.today())

    def to_dict(self):
        """
        Конвертировать объект формулы в словарь.

        Returns:
            dict: Словарь с данными формулы.
        """
        return {
            'id': self.id,
            'fullName': self.fullName,
            'expression': self.expression,
            'normalized': self.normalized,
            'date': self.date
        }
