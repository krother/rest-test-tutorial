"""
Entities:

Specify the data model used by the boundaries.
"""
from typing import Union

from pydantic import BaseModel


class SongRequest(BaseModel):
    name: str


class SongResponse(BaseModel):

    song_id: int
    title: str
    artist: str
    year: Union[int, None]
