"""
Repository:

Responsible for the data layer.
"""
import pymongo


def get_client():
    """Create a database connection"""
    return pymongo.MongoClient()


class SongRepository:

    def __init__(self):
        self.client = get_client()
        self.db = self.client["songdb"]
        
    def find_song_by_id(self, id: int):
        """Searches a song with exactly the correct id"""
        return self.db.songs.find_one({"song_id": id})

    def find_song_by_name(self, name: str):
        """Does a text search against the name field."""
        return self.db.songs.find_one({"name": name})
