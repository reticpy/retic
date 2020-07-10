# Werkzeug
from werkzeug.test import Client

# Pytest
import pytest

# Retic
from retic import App as app, Router

# Utils
from retic.services.general import _get_body_request

PATHS = [
    ("/withoutress")
]

CONTROLLERS = [
    lambda req, res: print("REST api Python example 🐍")
]


@pytest.fixture
def app_client():
    """Clear the app"""
    app.clear()
    """Returns an app client without routes"""
    return Client(app.application)


@pytest.fixture
def app_routes():
    """Clear the app"""
    app.clear()
    """Returns an app client with routes"""
    _router = Router()
    for _path in PATHS:
        """define a new path using the response from a path definition"""
        _router \
            .get(_path, *CONTROLLERS) \
            .get("/", *CONTROLLERS)
    app.use(_router)
    return Client(app.application)


@pytest.mark.lib_hooks
@pytest.mark.parametrize("path", PATHS)
def test_response_without_method(app_client, path):
    """we include a valid route and controllers"""
    app_iter, status, headers = app_client.get(path)
    assert status.upper() == '404 NOT FOUND', "A status 404 is necesary, but a status {} was got from the request".format(
        status)


@pytest.mark.lib_hooks
@pytest.mark.parametrize("path", PATHS)
def test_response_without_method_routes(app_routes, path):
    """we include a valid route and controllers"""
    app_iter, status, headers = app_routes.get(path)
    assert status.upper() == '200 OK', "A status 200 is necesary, but a status {} was got from the request".format(
        status)
    assert _get_body_request(
        app_iter) == '200 OK', "The default from the api when this one doesn't have routes is different to documentation"
