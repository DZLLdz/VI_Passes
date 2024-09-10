import os
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, Blueprint
from models import db
from flask_migrate import Migrate
from flask_restx import Api
# from routes import main
from dotenv import load_dotenv
from routes import api as routes_namespace
from swagger_models import api as swagger_models_namespace


dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{os.getenv('FSTR_DB_LOGIN')}:{os.getenv('FSTR_DB_PASS')}@{os.getenv('FSTR_DB_HOST')}:{os.getenv('FSTR_DB_PORT')}/{os.getenv('FSTR_DB_NAME')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

db.init_app(app)
migrate = Migrate(app, db)

with app.app_context():
    db.create_all()

api = Api(
    app,
    title="Документация API",
    version="1.0",
    description="Документация для вашего REST API",
    doc="/docs"  # URL для Swagger UI
)
api.add_namespace(routes_namespace, path='/api')
api.add_namespace(swagger_models_namespace)

if not app.debug:
    # Настройка логгирования в файл
    file_handler = RotatingFileHandler('error.log', maxBytes=10240, backupCount=10)
    file_handler.setLevel(logging.ERROR)

    # Формат логов
    formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    file_handler.setFormatter(formatter)

    # Добавляем обработчик в приложение
    app.logger.addHandler(file_handler)

if __name__ == '__main__':
    app.run(debug=True)
