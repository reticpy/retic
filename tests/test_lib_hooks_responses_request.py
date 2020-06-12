# Werkzeug
from werkzeug.test import Client

# Pytest
import pytest

# Retic
from retic import App, Router
from retic.lib.hooks.system.env import env
from retic.utils.general import get_body_request
from retic.utils.json import parse

PATHS = [
    ("/")
]
PATHS_SLASH = [
    ("/examples/")
]

CONTROLLERS = [
    # Check if the value is like as bytes, return string
    lambda req, res: res.ok({u'type': req.body.type, u'value': req.body.value if not isinstance(
        req.body.value, bytes) else req.body.value.decode("utf-8")})
]


@pytest.fixture
def app_routes():
    """Clear the app"""
    App.clear()
    """Returns an app client with routes"""
    _router = Router()
    for _path in PATHS+PATHS_SLASH:
        """define a new path using the response from a path definition"""
        _router \
            .get(_path, *CONTROLLERS) \
            .post(_path, *CONTROLLERS)
    App.use(_router)
    return Client(App.application)


"""Test about Body"""


@pytest.mark.lib_hooks
@pytest.mark.parametrize("path", PATHS)
def test_request_without_body(app_routes, path):
    """we include a valid route and controllers"""
    app_iter, status, headers = app_routes.get(path)
    _body = parse(get_body_request(app_iter))
    assert status.upper() == "200 OK"
    assert _body.get("type") == "undefiend"
    assert _body.get("value") == "undefiend"


@pytest.mark.lib_hooks
@pytest.mark.parametrize("path", PATHS)
def test_request_with_body_json(app_routes, path):
    """we include a valid route and controllers"""
    app_iter, status, headers = app_routes.post(path, json={'text': 'example'})
    _body = parse(get_body_request(app_iter))
    assert status.upper() == "200 OK"
    assert _body.get("type") == "json"
    assert _body.get("value") == {'text': 'example'}


@pytest.mark.lib_hooks
@pytest.mark.parametrize("path", PATHS)
def test_request_with_body_form(app_routes, path):
    """we include a valid route and controllers"""
    app_iter, status, headers = app_routes.post(path, data={'text': 'example'})
    _body = parse(get_body_request(app_iter))
    assert status.upper() == "200 OK"
    assert _body.get("type") == "form"
    assert _body.get("value") == {'text': 'example'}


@pytest.mark.lib_hooks
@pytest.mark.parametrize("path", PATHS)
def test_request_with_body_text(app_routes, path):
    """we include a valid route and controllers"""
    app_iter, status, headers = app_routes.post(
        path,
        data="{'text': 'example'}",
        content_type='text/plain'
    )
    _body = parse(get_body_request(app_iter))
    assert status.upper() == "200 OK"
    assert _body.get("type") == "text"
    assert _body.get("value") == "{'text': 'example'}"


@pytest.mark.lib_hooks
@pytest.mark.parametrize("path", PATHS)
def test_request_with_body_raw(app_routes, path):
    """we include a valid route and controllers"""
    app_iter, status, headers = app_routes.post(
        path,
        data="{'text': 'example'}",
        content_type='application/pdf'
    )
    _body = parse(get_body_request(app_iter))
    assert status.upper() == "200 OK"
    assert _body.get("type") == "raw"
    assert _body.get("value") == "{'text': 'example'}"


@pytest.mark.lib_hooks
@pytest.mark.parametrize("path", PATHS_SLASH)
def test_request_with_slash(app_routes, path):
    """we include a valid route and controllers"""
    app_iter, status, headers = app_routes.get(path)
    """Redirect to path without slash in the final"""
    _body = get_body_request(app_iter)
    assert status.upper() == "308 PERMANENT REDIRECT"
