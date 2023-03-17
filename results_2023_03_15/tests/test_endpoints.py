from fastapi.testclient import TestClient

from app import app

from song_finder.entity import SongRequest, SongResponse


class TestSongs:

    def setup_class(self):
        # run once per test run

    def test_hello():
        client = TestClient(app)
        response = client.get("/hello")
        assert response.status_code == 200
        assert response.json() == {"Hello": "World"}


    def test_find_song():
        client = TestClient(app)
        response = client.get("/songs/", json={"name": "3"})
        assert response.status_code == 200
        result = response.json()
        assert result["artist"] == "Stevie Wonder"


    def test_find_song_error():
        client = TestClient(app)
        response = client.get("/songs/", json={"name": "999"})
        assert response.status_code == 422  # BAD REQUEST
