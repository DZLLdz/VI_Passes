import json, pytest
from models import Users, db


def test_user_model(test_client, app_fix):
    with app_fix.app_context():
        user = Users(username='testuser', email='test@example.com', role='tourist')
        db.session.add(user)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            pytest.fail(f"Commit failed: {e}")
        retrieved_user = Users.query.get(user.id)
        assert retrieved_user.username == 'testuser'
        assert retrieved_user.email == 'test@example.com'
        assert retrieved_user.role == 'Test User'


def test_get_user(test_client, app_fix, init_database, sample_user):
    with app_fix.app_context():
        user, _ = init_database
        response = test_client.get(f'/api/users/{user.id}')
        data = json.loads(response.data)
        assert data['email'] == sample_user.email
        assert response.status_code == 200
        assert b'Test User' in response.data

