from flask import jsonify, request, render_template
from app.models import Formula
from app.db import db

from app.formulaCompare import compare_formula_trees, normalize_formula

def init_routes(app):
    """
    Домашняя страница

    Returns:
        Страница html
    """
    @app.route('/')
    def home_page():
        return render_template('index.html')
    
    """
    Инициализирует маршруты для приложения Flask.
    """
    @app.route('/api/formulas', methods=['GET'])
    def get_formulas():
        """
        Получить список всех формул из базы данных.

        Returns:
            Response: JSON-ответ, содержащий список формул.
        """
        formulas = Formula.query.all()
        return jsonify([formula.to_dict() for formula in formulas])

    @app.route('/api/formulas/<int:id>', methods=['GET'])
    def get_formula(id):
        """
        Получить формулу по её ID.

        Args:
            id (int): ID формулы для получения.

        Returns:
            Response: JSON-ответ с данными формулы.
        """
        formula = Formula.query.get_or_404(id)
        return jsonify(formula.to_dict())

    @app.route('/api/formulas', methods=['POST'])
    def add_formula():
        """
        Добавить новую формулу в базу данных.

        JSON-запрос:
            fullName (str): Название формулы.
            expression (str): Математическое выражение формулы.

        Returns:
            Response: JSON-ответ с данными созданной формулы.
        """
        data = request.get_json()
        if not data or 'fullName' not in data or 'expression' not in data:
            return jsonify({'error': 'Неверные данные'}), 400

        new_formula = Formula(
                            fullName=data['fullName'], 
                            normalized=normalize_formula(data['expression']),
                            expression=data['expression'])
        db.session.add(new_formula)
        db.session.commit()
        return jsonify(new_formula.to_dict()), 201

    @app.route('/api/formulas/<int:id>', methods=['PUT'])
    def update_formula(id):
        """
        Обновить существующую формулу по её ID.

        Args:
            id (int): ID формулы для обновления.

        JSON-запрос:
            fullName (str): Название формулы.
            expression (str): Математическое выражение формулы.

        Returns:
            Response: JSON-ответ с обновлёнными данными формулы.
        """
        formula = Formula.query.get_or_404(id)
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Неверные данные'}), 400

        formula.fullName = data.get('fullName', formula.fullName)
        formula.expression = data.get('expression', formula.expression)
        formula.normalized = normalize_formula(data.get('expression', formula.expression))
        db.session.commit()
        return jsonify(formula.to_dict())

    @app.route('/api/formulas/<int:id>', methods=['DELETE'])
    def delete_formula(id):
        """
        Удалить формулу по её ID.

        Args:
            id (int): ID формулы для удаления.

        Returns:
            Response: JSON-ответ с подтверждением удаления.
        """
        formula = Formula.query.get_or_404(id)
        db.session.delete(formula)
        db.session.commit()
        return jsonify({'message': f'Формула с ID {id} удалена'}), 200
    
    @app.route('/api/formulas/compare', methods=['POST'])
    def compare_formula():
        """
        Проверка формулы на совпадения.

        JSON-запрос:
            expression (str): Математическое выражение формулы.

        Returns:
            Response: JSON-ответ
        """
        return jsonify({'message': f'Ы'}), 200
