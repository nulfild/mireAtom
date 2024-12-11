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


## Описание API

### Сущность Формула

Поля:

- id (int): Уникальный идентификатор формулы
- fullName (str): Название формулы
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

3. Добавить новую формулу в базу данных

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

4. Обновить существующую формулу по её ID

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

5. Удалить формулу по её ID

DELETE-запрос: `/api/formulas/<int:id>`

Ответ: Подтверждение

Пример запроса: `/api/formulas/1`

Пример ответа:
```
{
	"message": "Формула с ID 1 удалена"
}
```

6. Проверка формулы на совпадения

POST-запрос: `/api/formulas/compare`

Ответ: Какой-то ответ

Пример тела запроса:
```
{
	"expression": "\\sqrt{2}"
}
```
Пример ответа:
```

```