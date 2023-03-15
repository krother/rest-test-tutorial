
from fastapi.testclient import TestClient

from app import app


def test_hello():
    client = TestClient(app)
    response = client.get('/hello')
    assert response.status_code == 200
    assert response.json() == {'Hello': 'World'}
