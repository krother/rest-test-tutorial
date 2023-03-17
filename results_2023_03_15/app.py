from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from song_finder.boundary import find_song
from song_finder.entity import SongRequest, SongResponse


app = FastAPI()


@app.exception_handler(IndexError)
def db_error_handler(request: Request, exc: IndexError):
    print("log message", str(exc))
    return JSONResponse(
        status_code=422,
        content={
            "message": f"an error occured but I'm not telling you which one. Sorry."
        },
    )


@app.get("/hello")
def hello():
    return {"Hello": "World"}


@app.get("/songs", response_model=SongResponse)
def find_song_endpoint(query: SongRequest) -> SongResponse:
    return find_song(query)
