import os
from dotenv import load_dotenv
import pytest
import logging
from sqlalchemy.exc import SQLAlchemyError
from main import app, db
from models import Users, Passes, ActivitiesTypes

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


@pytest.fixture(scope='module')
def app_fix():
    app_fix = app('testing')
    with app_fix.app_context():
        yield app_fix


@pytest.fixture(scope='module')
def test_client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{os.getenv('FSTR_DB_LOGIN')}:{os.getenv('FSTR_DB_PASS')}@{os.getenv('FSTR_DB_HOST')}:{os.getenv('FSTR_DB_PORT')}/{os.getenv('FSTR_DB_NAME')}"

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        # with app.app_context():
        #     db.drop_all()


@pytest.fixture(scope='module')
def init_database(test_client, sample_user):
    user = sample_user
    db.session.add(user)
    db.session.commit()
    sample_pass = Passes(
        users_id=user.id,
        coords_id=1,
        beautyTitle="Test Title",
        title="Test Title",
        other_titles="Test Other Titles",
        connect=[],
        level_winter="oneA",
        level_spring="oneB",
        level_summer="twoA",
        level_autumn="z1"
    )
    db.session.add(sample_pass)
    db.session.commit()
    return sample_user, sample_pass


@pytest.fixture(scope='module')
def sample_user(test_client):
    user = Users(username='testuser', email='test@yandex.ru', role='tourist', atype=ActivitiesTypes)
    try:
        db.session.add(user)
        db.session.commit()
        logging.info("User added successfully.")
    except SQLAlchemyError as e:
        db.session.rollback()
        logging.error(f"Error adding user: {e}")
        raise
    return user


@pytest.fixture(scope='module')
def sample_pass(test_client, sample_user):
    new_pass = Passes(
        users_id=sample_user,
        coords_id=1,
        beautyTitle="Beauty Title 2",
        title="Test Title 2",
        other_titles="Test Other Titles",
        connect=[],
        level_winter="oneA",
        level_spring="oneA",
        level_summer="twoA",
        level_autumn="twoA"
    )
    db.session.add(new_pass)
    db.session.commit()
    return new_pass
