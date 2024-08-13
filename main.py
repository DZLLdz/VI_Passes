import os
from flask import Flask
from models import db
from routes import main
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{os.getenv('FSTR_DB_LOGIN')}:{os.getenv('FSTR_DB_PASS')}@{os.getenv('FSTR_DB_HOST')}:{os.getenv('FSTR_DB_PORT')}/{os.getenv('FSTR_DB_NAME')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

app.register_blueprint(main)

with app.app_context():
    db.create_all()


if __name__ == '__main__':
    app.run(debug=True)
