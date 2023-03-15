
import pymongo


class SongRepository:

    def __init__(self):
        self.client = self.get_client()
        self.db = self.client["songdb"]
        
    def get_client(self):
        """Create a database connection"""
        return pymongo.MongoClient()
    
    def find_song_by_id(self, id: int) -> Union[dict, None]:
        """Searches a song with exactly the correct id"""
        return self.db.songs.find_one({"id": id})

    def find_song_by_name(self, name: str) -> Union[dict, None]:
        """Does a text search against the name field."""
        return self.db.songs.find_one({"name": name})
