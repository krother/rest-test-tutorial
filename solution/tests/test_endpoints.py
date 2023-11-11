
from fastapi.testclient import TestClient

from app import app


def test_hello():
    client = TestClient(app)
    response = client.get('/hello')
    assert response.status_code == 200
    assert response.json() == {'Hello': 'World'}


def test_find():
    client = TestClient(app)
    response = client.post('/songs', json={"name": "3"})
    assert response.status_code == 200
    assert response.json() == {
        'song_id': 3,
        'artist': 'Stevie Wonder',
        'title': 'You are the sunshine of my life', 
        'year': None,
    }


def test_find_fail():
    client = TestClient(app)
    response = client.post('/songs', json={"name": "999"})
    assert response.status_code == 422
