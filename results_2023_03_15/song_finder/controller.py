from song_finder.entity import SongRequest, SongResponse
from song_finder.repository import SongRepository

import json
import os
import re


def execute_query(query: SongRequest) -> SongResponse:
    """Finds a song with the given query parameters"""
    repo = SongRepository()
    if re.match(r"\d+", query.name):
        song = repo.find_song_by_id(int(query.name))
    else:
        song = repo.find_song_by_name(query.name)
    if song:
        return SongResponse(**song)


# def execute_query(query: SongRequest) -> SongResponse:
#     """Finds a song with the given query parameters"""
#     # load song database
#     path = os.path.split(__file__)[0]
#     songdb = json.load(open(os.path.join(path, 'songs.json')))
#
#     # search song by id or title
#     for song in songdb:
#         if (
#                 str(song["song_id"]) == query.name or
#                 query.name.lower() in song["title"].lower()
#         ):
#             return SongResponse(**song)
