from flask import jsonify, request, render_template
from flask_cors import cross_origin
from app.models import Formula
from app.db import db

from app.formulaCompare import compare_formula_trees, normalize_formula

def init_routes(app):
    """
    Инициализирует маршруты для приложения Flask
    """
    
    @app.route('/')
    @cross_origin()
    def home_page():
        """
        Домашняя страница

        Returns:
            Страница html
        """
        return render_template('index.html')
    
    @app.route('/formula')
    @cross_origin()
    def admin_page():
        """
        Страница редактирвоания БД

        Returns:
            Страница html
        """
        return render_template('admin.html')
    
    @app.route('/api/docs')
    def get_docs():
        """
        Документация API

        Returns:
            Страница html
        """
        return render_template('swaggerui.html')
    
    @app.route('/api/formulas', methods=['GET'])
    @cross_origin()
    def get_formulas():
        """
        Получить список всех формул из базы данных

        Returns:
            Response: JSON-ответ, содержащий список формул
        """
        formulas = Formula.query.all()
        return jsonify([formula.to_dict() for formula in formulas])

    @app.route('/api/formulas/<int:id>', methods=['GET'])
    @cross_origin()
    def get_formula_by_id(id):
        """
        Получить формулу по её ID

        Args:
            id (int): ID формулы для получения

        Returns:
            Response: JSON-ответ с данными формулы
        """
        formula = Formula.query.get_or_404(id)
        return jsonify(formula.to_dict())
    
    @app.route('/api/formulas/<string:fullName>', methods=['GET'])
    @cross_origin()
    def get_formula_by_fullName(fullName):
        """
        Получить формулу по названию

        Args:
            fullName (str): Название формулы для получения

        Returns:
            Response: JSON-ответ с данными формулы
        """
        formulas = Formula.query.filter(Formula.fullname.ilike(f'%{fullName}%')).all()
        return jsonify([formula.to_dict() for formula in formulas])


    @app.route('/api/formulas', methods=['POST'])
    @cross_origin()
    def add_formula():
        """
        Добавить новую формулу в базу данных

        JSON-запрос:
            fullName (str): Название формулы
            expression (str): Математическое выражение формулы

        Returns:
            Response: JSON-ответ с данными созданной формулы
        """
        data = request.get_json()
        if not data or 'fullName' not in data or 'expression' not in data:
            return jsonify({'error': 'Неверные данные'}), 400
        
        formula = Formula.query.filter(Formula.fullname.ilike(data['fullName'])).first()
        if formula:
            return jsonify({'answer': 'Формула с таким названием уже существует'}), 400

        new_formula = Formula(
                            fullname=data['fullName'], 
                            normalized=normalize_formula(data['expression']),
                            expression=data['expression'])
        db.session.add(new_formula)
        db.session.commit()
        return jsonify(new_formula.to_dict()), 201

    @app.route('/api/formulas/<int:id>', methods=['PUT'])
    @cross_origin()
    def update_formula(id):
        """
        Обновить существующую формулу по её ID

        Args:
            id (int): ID формулы для обновления

        JSON-запрос:
            fullName (str): Название формулы
            expression (str): Математическое выражение формулы

        Returns:
            Response: JSON-ответ с обновлёнными данными формулы
        """
        formula = Formula.query.get_or_404(id)
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Неверные данные'}), 400
        
        last_formula = Formula.query.filter(Formula.fullname.ilike(data['fullName'])).first()
        if last_formula and formula.id != last_formula.id:
            return jsonify({'answer': 'Формула с таким названием уже существует'}), 400

        formula.fullName = data.get('fullName', formula.fullname)
        formula.expression = data.get('expression', formula.expression)
        formula.normalized = normalize_formula(data.get('expression', formula.expression))
        db.session.commit()
        return jsonify(formula.to_dict())

    @app.route('/api/formulas/<int:id>', methods=['DELETE'])
    @cross_origin()
    def delete_formula(id):
        """
        Удалить формулу по её ID

        Args:
            id (int): ID формулы для удаления

        Returns:
            Response: JSON-ответ с подтверждением удаления
        """
        formula = Formula.query.get_or_404(id)
        db.session.delete(formula)
        db.session.commit()
        return jsonify({'message': f'Формула с ID {id} удалена'}), 200
    
    @app.route('/api/formulas/compare', methods=['POST'])
    @cross_origin()
    def compare_formula():
        """
        Проверка формулы на совпадения

        JSON-запрос:
            expression (str): Математическое выражение формулы

        Returns:
            Response: JSON-ответ
        """
        data = request.get_json()
        if not data or 'expression' not in data:
            return jsonify({'error': 'Неверные данные'}), 400
        
        formula = data['expression']

        formulas = Formula.query.all()
        
        result = []
        for exist_formula in formulas:
            try:
                compare_result = compare_formula_trees(formula, exist_formula.expression)
                if 'error' in compare_result:
                    error = compare_result['error']
                    print(f'При проверки формул ({formula} и {exist_formula}) произошла ошибка: {error}')
                    continue
                result.append(compare_result)
            except Exception as e:
                print(f'При проверки формул ({formula} и {exist_formula}) произошла ошибка: {e}')

        if len(result) == 0:
            return jsonify({'answer': 'Совпадений не найдено'}), 200
        
        result = sorted(result, key=lambda res: res['similarity'], reverse=True)[0]

        if result['similarity'] == 0:
            return jsonify({'answer': 'Совпадений не найдено'}), 200

        return jsonify(result), 200
