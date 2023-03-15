
# REST-Test Tutorial

**Organizing test data, fixtures and Mocks in Python**

![laptop generated with deepai.org](title.jpeg)

## Goal:

In this tutorial, you learn to write tests for a Python REST API powered by a database.
You will use the `pytest` framework to create Unit Tests, Integration Tests and end-to-end tests.
The tutorial will cover:

- code structures that make code well-testable
- organizing test data for use with and without
- efficient use of fixtures
- error handling in tests
- the pros and cons of mocking
- building a small test database

The tutorial will be rounded off with a few useful tools that make your life easier when testing Python code.

![types of tests](test_types.svg)

----

## Target Audience

Developers who would like to test Python applications.
Basic knowledge of Python is sufficient.
You don't need prior experience with automated testing.

----

## 1. Preparations

This tutorial should work on Python 3.9 and above.
In the files you find two folders:

* `exercise/` – starting point to build tests step by step
* `solution/` – everything done and working

To use the code, install the dependencies:

    pip install -r requirements.txt

Python needs to import the app, so you need to include the main directory of the project in the import path of Python, e.g. on Ubuntu:

    export PYTHONPATH=$PYTHONPATH:$HOME/projects/rest-testtutorial/exercise

Go to the folder `exercise/` and start the server with:

    uvicorn app:app

Go to [http://localhost:8000/docs](http://localhost:8000/docs).
You should see that Swagger is up.

----

## 2. A first Unit Test

The most important tests in a REST API are tests against the endpoints.
FastAPI supports a lightweight test client that integrates nicely with `pytest`.

In the folder `tests/` you find a file `test_endpoints.py` containing a test against the enpoint `/hello`.
Run the test by typing:

    pytest

You should see some output and a message like:

    ============================== 1 passed in 0.15s ===============================

Write another test against the endpoint `/songs`

    :::python3
    response = client.get('/songs', json={"name": "3"})

----

## 3. Define Entities

To improve the program further, we will create a structure that makes the code easier to test.
In this tutorial, we will use the **BCE (Boundary-Control-Entity) Pattern**.
This pattern defines clear responsibilities for components.
In the `song_finder/`, we will split the initial app into 3 files:

* `entity.py` : contains the data objects that we send around
* `boundary.py` : contains toplevel functions
* `control.py` : does the actual work

In [entity.py](exercises/song_finder/entity.py), we define an Entity for a request and its response.
Both are using `pydantic`, a library that will do type checking at runtime for us.

Modify the endpoint `/song` so that it uses the entities:

    :::python3
    from song_finder.entity import SongRequest, SongResponse

    ...
    @app.get(
        "/songs",
        response_model=SongResponse
    )
    def find_song(query: SongRequest) -> SongResponse:
        ...
        return SongResponse(**song)

We can add a Unit Test for the entities as well:

    :::python3
    def test_song_response():
        SongResponse(
            song_id=7,
            title="I'm in love with the shape of you",
            author="Ed Sheeran"
        )

Run the Unit Tests to make sure everything works.

----

### 4. Define Boundaries

In the boundary, we place the public access points for the song finder.
Ideally, other parts of the program communicate only with the boundary.
Boundaries are usually short. They mainly delegate work to the controller, but may also do some logging and error handling.

It makes sense to have a toplevel function that does not know anything about the API.
In [boundary.py](exercises/song_finder/boundary.py) you find a header to which you can move the code for the `songs/` endpoint from `app.py`.

Now we can add a test against the new boundary:

    :::python3
    from song_finder.boundary import find_song
    from song_finder.entity import SongRequest, SongResponse


    def test_find_song_boundary():
        request = SongRequest(name=3)
        song = find_song(request)
        assert type(song) == SongResponse
        assert song.song_id == 3
        assert song.artist == "Stevie Wonder"
        assert song.title.startswith("You are the sunshine")

Move all the code from `app.py` that is not absolutely necessary for the API to the boundary.

#### Note:

The API endpoints conceptually also belong to the boundary.
One could move them to the boundary module.
However, we don't do that for now, because this would make `app.py` a lot more complicated.

----

### 5. Controller

Writing a controller is easy.
Everything that is not a boundary can be moved into the controller.
In [controller.py](exercises/song_finder/controller.py) you find a function header.

Move code from the boundary function that does the work into the controller.
 Complete the refactoring and run the tests again.

----

## 6. Fixtures

Before we write more tests, we make our life a little easier.
We will prepare frequently used objects as **fixtures**.
The fixtures are created before every test. 

Let's use one fixture for an example request and response.
You find one fixture for `SongRequest` in [conftest.py](exercises/tests/conftest.py) already.
Add the other one for `SongResponse`.

With fixtures in place our test code becomes shorter.
`pytest` finds and executes all fixtures in `conftest.py` automatically.
We can now test our boundaries very easily:

    :::python3
    def test_find_song(song_request, song_response):
        assert find_song(song_request) == song_response

When your API fixtures become bigger, you could load the data for the fixtures from JSON files.

----

## 7. Error Handling in Tests

There are two types of errors that you want to test against: **error codes of the API** and **errors in the boundary functions**. Both are important.
You want to test against errors in the endpoints, because they are public.
You also want to test against the boundary functions, because they are easier to debug.

Let's start with the boundary function.
We would expect that we get an `IndexError` if a song can't be found.
In a test function checking for **Python Exceptions** one would use the `pytest.raises' Context Manager:

    :::python3
    def test_find_song_error():
        with pytest.raises(IndexError):
            request = SongRequest(name="999")
            find_song(request)


If we want to check for errors in the API, we can simply check the **HTTP status code** of the requests.
The syntax of such a test is the same as for the endpoint test we already have.

Often you don't want to expose your internal errors to the API users.
In that case it makes sense to define an error handler in `app.py`. 
Here, you can catch errors and replace them by the responses of your choice.

    :::python3
    from fastapi import FastAPI, Request
    from fastapi.responses import JSONResponse

    @app.exception_handler(IndexError)
    def db_error_handler(request: Request, exc: IndexError):
        print("log message", str(exc))
        return JSONResponse(
            status_code=422,
            content={"message": f"an error occured but I'm not telling you which one. Sorry."},
        )

----

## 8. Mocking a Database

As you probably noticed, we are loading the song data from JSON again for each request.
Let's use a database instead.
In [repository.py](exercises/tests/repository.py) you find an example for a database adapter for MongoDB.
It uses the popular **Repository Pattern**, so you could exchange the type of database easily without the rest of the program knowing.

To test a REST API connected to a database, you may want to test without an actual database.
A lighter infrastructure is easier to maintain and your tests will run faster.
Therefore, we will replace the database with a **Mock**.
First, we will use `mongomock` to create a mock database that does most things that MongoDB does but is using in-memory data behind the scenes.
Second, the module `unittest.mock` allows us to sneak our mock database into the repository temporarily (it is replaced after the test).

A fully mocked test looks like this:

    :::python3
    from mongomock import MongoClient
    from unittest.mock import patch

    def test_mock_db(song_request, songs, mocker:MockerFixture):
        client = MongoClient()
        client["songdb"].songs.insert_many(songs)
        
        mocker.patch("song_finder.repository.get_client", return_value=client)
        song = find_song(song_request)
        assert song.song_id == 3

Define `songs` as a fixture in `conftest.py`.
Place a copy of `songs.json` in the tests folder. It is good to store test data there.

An alternative would be to mock the entire `SongRepository` class instead and replace it with something lighter (e.g. SQLite).
The outcome

----

## 9. Integration Test 

Using a mock database gets you only this far.
First, mock databases like `mongomock` do not implement all features of the real MongoDB.
If you depend on advanced MongoDB features like pipelines or GeoIndices, your mock will fail.
With the SQL equivalent you can expect similar effect.
Second, you might want to test the entire product before deploying it.

We could start a MongoDB in a docker container for local testing:

    docker run -d -it -p 27017:27017 mongo

The vanilla `MongoClient()` constructor will find a local database without having to configure anything.
For our tests to run you might want to connect to the database locally and insert the data manually:

    docker exec -it mongodb mongo

    use songdb
    db.songs.insert_many(PASTE songs.json HERE)

Now once again run pytest and see whether the tests find your data.

Here is a recipe to run the integration tests in a more consistent way:

1. write a `Dockerfile` for building the REST-API container
2. write a docker-compose file that starts the database and rest-api container
3. configure the database connection dynamically (e.g. via environment variables)
4. execute `pytest` inside the container
5. copy the test results out of the container
6. write a bash script that connects everything

----

## 10. End-to-End Test

Because I am not an HTML expert, I asked my assistant to write a front end given the following instructions:

   write a HTML page that contains a form that asks the user for a song name and then uses JavaScript to send a GET request to a REST API endpoint http://localhost:8000/songs/{name}

The result required only minimal adjustment. You find it in [index.html](index.html).

To allow the browser to talk to the API, we need to configure CORS.
Because this is not a tutorial on security, we simply allow everything.
Add the following to `app.py`:

    from fastapi.middleware.cors import CORSMiddleware    
    ...
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

Now it should be possible to use the service from a browser.
But how to test it?

For a long time, **Selenium** has been the gold standard in broser automation.
More recently, the more modern library **playwright** is gaining momentum.
In addition to the `pip` installation you need to run:

   playwright install

Playwright automates most steps you can do in **Chrome, Firefox** and **Safari**.
For a sneak peek let's record a browser session with the **Test Generator**.

Start it using:

    playwright codegen index.html

Copy the resulting code and replay it with Python.
Note that the REST API needs to be running.

You might want to add a few lines to rework the code into a test that `pytest` can execute, e.g.:

    browser = p.firefox.launch(headless=False)
    page = browser.new_page()
    page.goto("file:///home/kristian/projects/rest_test_tutorial/index.html")
    page.is_visible('body')

    assert "Stevie Wonder" in page.inner_html('body')


----

## 8. Useful tools

There are a few options to improve the `pytest` call.
A basic thing are the `-s` and `-v` options.
The `-s` lets you see the standard output (useful for debugging with `print`).
The `-v` makes the output more verbose.

If you have the `pytest-coverage` library installed, you can calculate what percentage of the code is covered by tests.
This metric has its issues but it is a lot better than nothing.

The complete call to `pytest` is:

    pytest -s -v --cov song_finder/

You may also use `black` to clean up your code so that it adheres to the PEP8 style guideline.

    black .

----

## Conclusion

This is a small testing cycle with many parts you would also find in a big software project.

Here are a few recommended links for further reading:

* [fastapi.tiangolo.com/](https://fastapi.tiangolo.com/) – framework for REST APIs
* [www.fullstackpython.com/](https://www.fullstackpython.com/) – Python friendly technologies for web development
* [www.youtube.com/watch?v=WpkDN78P884&t=2s](https://www.youtube.com/watch?v=WpkDN78P884) – Uncle Bob explaining the BCE Pattern

----

(c) 2023 Dr. Kristian Rother

you may reuse and modify the material here freely under the conditions of the MIT License.
See LICENSE.TXT for details.
