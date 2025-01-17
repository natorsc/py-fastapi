from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)


def test_main_status_code():
    response = client.get('/')
    assert response.status_code == 200


def test_main_json_reponse():
    response = client.get('/')
    assert response.json() == {'msg': 'Hello World!'}
