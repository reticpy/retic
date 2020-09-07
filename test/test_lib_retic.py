# Pytest
import pytest

# Werkzeug
from werkzeug.test import Client

# Retic
from retic import App as app, Router

PATHS = [
    ("/"),
]
PATHS_ROUTES = [
    ("/endpoint")
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
def app_without_client():
    """Clear the app"""
    app.clear()
    """Returns an app client with routes"""
    _router = Router()
    for _path in PATHS+PATHS_SLASH+PATHS_ROUTES:
        """define a new path using the response from a path definition"""
        _router \
            .get(_path, *CONTROLLERS) \
            .post(_path, *CONTROLLERS)
    app.use(_router)
    return app


@pytest.mark.lib
def test_config_attribute():
    """Clear the configuration"""
    app.config.clear()
    """Check that the variables aren't exists"""
    assert app.config.get("APP_LANG") == None
    assert app.config.get("APP_HOSTNAME") == None
    """we include a basic setting to app"""
    app.config.set("APP_LANG", "en_US")
    app.config.set("APP_HOSTNAME", "localhost")
    """Check if this value was saved in the object"""
    assert app.config.get("APP_LANG") == "en_US", \
        "The value from the configuration item is different to value saved"
    assert app.config.get("APP_HOSTNAME") == "localhost", \
        "The value from the configuration item is different to value saved"


@pytest.mark.lib
def test_config_attribute():
    """Clear the configuration"""
    app.config.clear()
    """We don't include a basic setting to app and check if this value wasn't saved in the object"""
    assert app.config.get("APP_LANG") == None


@pytest.mark.lib
def test_config_from_object():
    """Clear the configuration"""
    app.config.clear()
    """Check that the variables aren't exists"""
    assert app.config.get("APP_LANG") == None
    """Set the settings from an object"""
    app.config.from_object({u'APP_LANG': "en_US"})
    """check if this value exists"""
    assert app.config.get("APP_LANG") == "en_US", \
        "The value from the configuration item is different to value saved"

@pytest.mark.lib
def test_config_clear():
    """Set the settings from an object"""
    app.config.from_object({u'APP_LANG': "en_US"})
    """check if this value exists"""
    assert app.config.get("APP_LANG") == "en_US", \
        "The value from the configuration item is different to value saved"
    """Clear the configuration"""
    app.config.clear()
    """Check that the variables aren't exists"""
    assert app.config.get("APP_LANG") == None


"""Test about main App"""


@pytest.mark.lib_api
@pytest.mark.parametrize("path", PATHS_ROUTES)
def test_request_clear_app(app_without_client, path):
    _app = Client(app_without_client.application)
    """get a request when the app has routes"""
    app_iter, status, headers = _app.get(path)
    assert status.upper() == "200 OK"
    """we clear the information of App"""
    app_without_client.clear()
    """get a request when the app hasn't routes"""
    app_iter, status, headers = _app.get(path)
    assert status.upper() == "404 NOT FOUND"
