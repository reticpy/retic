# Werkzeug
from werkzeug.test import Client

# Pytest
import pytest

# Retic
from retic import App, Router

# Utils
from tests.utils.general import get_body_request

PATHS = [
    ("/withoutress")
]

CONTROLLERS = [
    lambda req, res: print("REST api Python example 🐍")
]


@pytest.fixture
def app():
    """Returns a HttpMethod"""
    _app = Client(App.application)
    return _app


@pytest.fixture
def app_routes():
    """Returns a HttpMethod"""
    _router = Router()
    for _path in PATHS:
        """define a new path using the response from a path definition"""
        _router \
            .get(_path, *CONTROLLERS) \
            .get("/", *CONTROLLERS)
    App.use(_router)
    _app = Client(App.application)
    return _app


@pytest.mark.lib_responses
@pytest.mark.parametrize("path", PATHS)
def test_response_without_method(app, path):
    # we include a valid route and controllers
    app_iter, status, headers = app.get(path)
    assert status == '404 Not found', "A status 404 is necesary, but a status {} was got from the request".format(
        status)
    assert get_body_request(
        app_iter) == "error: The HTTP method GET doesn't exist", "The default from the api when the path doesn't exist is different to documentation"


@pytest.mark.lib_responses
@pytest.mark.parametrize("path", PATHS)
def test_response_without_method_routes(app_routes, path):
    # we include a valid route and controllers
    app_iter, status, headers = app_routes.get(path)
    assert status == '200 OK', "A status 200 is necesary, but a status {} was got from the request".format(
        status)
    assert get_body_request(
        app_iter) == '200 OK', "The default from the api when this one doesn't have routes is different to documentation"
