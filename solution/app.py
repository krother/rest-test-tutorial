
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from song_finder.entity import SongRequest, SongResponse
from song_finder.boundary import find_song, SongFinderError


app = FastAPI()


@app.exception_handler(SongFinderError)
def db_error_handler(request: Request, exc: SongFinderError):
    """
    FastAPIs internal error handler allows to connect
    custom Exceptions to HTTP reponses
    """
    print("log message", str(exc))
    return JSONResponse(
        status_code=422,
        content={"message": f"an error occured: {exc}\n"},
    )


@app.get("/hello")
def hello():
    return {"Hello": "World"}


@app.post(
    "/songs",
    response_model=SongResponse
    )
def find_song_endpoint(query: SongRequest) -> SongResponse:
    return find_song(query)
