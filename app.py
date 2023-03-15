from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from boundary import get_song


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(IndexError)
def db_error_handler(request: Request, exc: IndexError):
    print("log message", str(exc))
    return JSONResponse(
        status_code=404,
        content={"message": f"error occured"},
    )



@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/songs/{name}")
def read_item(name: str):
    return get_song(name)


def get_song(song_id: int) -> SongResponse:
    """Finds a song with the given id"""
    # DB Query
    for d in DOCS:
        if d["song_id"] == int(song_id):
            return SongResponse(**d)
    raise IndexError(f"song {song_id} not found!")
