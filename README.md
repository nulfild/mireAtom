# mireAtom

## Запуск локально

Для запуска необходимо создать файл .env в корне проекта (пример можно найти в файле envExample.txt)

Создание виртуального окружения:
```
python -m venv venv
```

Активация виртуального окружения:
```
venv\Scripts\activate.bat
```

Установка необходимых пакетов:
```
pip install -r requirements.txt
```

Запуск приложения:
```
python run.py
```

Выключение виртуального окружения:
```
deactivate
```

## Запуск с помощью Docker
```bash
docker-compose up
```
В фоне:
```bash
docker-compose up -d
```

## Описание Сервера

Главная страница доступна по URL: `http://localhost:5000`

Страница редактирования бд: `http://localhost:5000/formula`

API Сервера: `http://localhost:5000/api`

Документация API: `http://localhost:5000/api/docs`

## Описание API

### Сущность Формула

Поля:

- id (int): Уникальный идентификатор формулы (уникально)
- fullName (str): Название формулы (уникально)
- normalized (str): Нормализованная формула
- expression (str): Математическое выражение формулы
- date (datetime): Дата создания формулы

### Запросы

1. Получить список всех формул из базы данных

GET-запрос: `/api/formulas`

Ответ: Список формул

Пример ответа:
```
[
	{
		"date": "Wed, 11 Dec 2024 17:33:09 GMT",
		"expression": "\\sqrt{2}",
		"fullName": "Test",
		"id": 2,
		"normalized": "\\sqrt{2}"
	}
]
```

2. Получить формулу по её ID

GET-запрос: `/api/formulas/<int:id>`

Ответ: Формула

Пример запроса: `/api/formulas/1`

Пример ответа:
```
{
	"date": "Wed, 11 Dec 2024 17:33:09 GMT",
	"expression": "\\sqrt{2}",
	"fullName": "Test",
	"id": 2,
	"normalized": "\\sqrt{2}"
}
```

3. Получить формулу по её названию

GET-запрос: `/api/formulas/<string:fullName>`

Ответ: Формула

Пример запроса: `/api/formulas/Test`

Пример ответа:
```
[
	{
		"date": "Wed, 11 Dec 2024 17:33:09 GMT",
		"expression": "\\sqrt{2}",
		"fullName": "Test",
		"id": 2,
		"normalized": "\\sqrt{2}"
	}
]
```

4. Добавить новую формулу в базу данных

POST-запрос: `/api/formulas`

Ответ: Формула

Пример тела запроса:
```
{
	"fullName": "Test",
	"expression": "\\sqrt{2}"
}
```
Пример ответа:
```
{
	"date": "Wed, 11 Dec 2024 17:33:09 GMT",
	"expression": "\\sqrt{2}",
	"fullName": "Test",
	"id": 2,
	"normalized": "\\sqrt{2}"
}
```

Если формула с таким названием уже существует, то вернется ответ:
```
{
	"answer": "Формула с таким названием уже существует"
}
```

5. Обновить существующую формулу по её ID

PUT-запрос: `/api/formulas/<int:id>`

Ответ: Формула

Пример запроса: `/api/formulas/1`

Пример тела запроса:
```
{
	"fullName": "Test2",
	"expression": "\\sqrt{2}"
}
```
Пример ответа:
```
{
	"date": "Wed, 11 Dec 2024 17:30:35 GMT",
	"expression": "\\sqrt{2}",
	"fullName": "Test2",
	"id": 1,
	"normalized": "\\sqrt{2}"
}
```

Если формула с таким названием уже существует, то вернется ответ:
```
{
	"answer": "Формула с таким названием уже существует"
}
```

6. Удалить формулу по её ID

DELETE-запрос: `/api/formulas/<int:id>`

Ответ: Подтверждение

Пример запроса: `/api/formulas/1`

Пример ответа:
```
{
	"message": "Формула с ID 1 удалена"
}
```

7. Проверка формулы на совпадения

POST-запрос: `/api/formulas/compare`

Ответ: Параметры совпадения:
- commonExpressions - Совпадающие части
- finded - Найденная в бд формула
- normalized - Нормализованный вид исходной формулы
- similarity - Процент совпадения

Пример тела запроса:
```
{
	"expression": "\\sqrt{2}"
}
```
Пример ответа:
```
{
	"commonExpressions": [
		"a^{2} + 2 a b + b^{2}",
		"a^{2}",
		"b^{2}",
		"2 a b"
	],
	"finded": "x^2 + 2xy + y^2",
	"normalized": "a^{2} + 2 a b + b^{2}",
	"similarity": 100.0
}
```
Если совпадений не найдено (процент совпадения = 0), то возвращается:
```
{
	"answer": "Совпадений не найдено"
}
```