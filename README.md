# Проект API_Vi_passes

## Описание

Этот проект в разработке API для хранения информации о перевалах.
API разрабатывается с использованием Flask и документируется с помощью Swagger.
В настоящее время ведется тестирование и исправление ошибок

## Установка

### Требования

- Python 3.x
- pip
  - Flask-3.0.3
  - Jinja2-3.1.4
  - MarkupSafe-2.1.5
  - Werkzeug-3.0.3
  - blinker-1.8.2
  - click-8.1.7
  - itsdangerous-2.2.0
  - psycopg2-2.9.9
  - Flask-SQLAlchemy-3.1.1
  - sqlalchemy-2.0.32
  - typing-extensions-4.12.2
  - python-dotenv-1.0.1
  - certifi-2024.7.4
  - charset-normalizer-3.3.2
  - idna-3.7
  - requests-2.32.3
  - urllib3-2.2.2
  - Flask-Migrate-4.0.7
  - Mako-1.3.5
  - alembic-1.13.2
  - marshmallow-3.21.3
  - marshmallow-sqlalchemy-1.1.0
  - packaging-24.1 

  - flask-restx-1.3.0
    - aniso8601-9.0.1
    - attrs-24.2.0
    - importlib-resources-6.4.4
    - jsonschema-4.23.0
    - jsonschema-specifications-2023.12.1
    - pytz-2024.1
    - referencing-0.35.1
    - rpds-py-0.20.0
  - pytest-flask-1.3.0
    - pytest-8.3.2
    - iniconfig-2.0.0
    - pluggy-1.5.0




### Установка зависимостей
пошагово выполняем:
   ```bash
   git clone https://github.com/DZLLdz/VI_Passes
   cd VI_Passes
   python -m venv venv
   source venv/bin/activate  # Для Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```
### Запускаем сервер
   ```bash
   python main.py runserver
   ```

### Документация SWAGGER
будет доступна по адресу:
   ```bash
   http://localhost:5000/docs 
   ```