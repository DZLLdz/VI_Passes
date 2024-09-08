import json


def test_hello_world(test_client):
    response = test_client.get('/api/hello')
    assert response.status_code == 200
    assert b'Hello, World!' in response.data
    assert json.loads(response.data) == {"message": "Hello, World!"}
