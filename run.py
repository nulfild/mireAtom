from app import create_app
from app.db import db
import os

PORT = os.getenv('PORT', 5010)

app = create_app()

if __name__ == '__main__':
    # Инициализация базы данных
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=PORT, threaded=True)
