# Pytest
import pytest

# Retic
from retic.lib.router import httpmethod, router

PATHS = [
    ("/withoutres"),
    ("/")
]

CONTROLLERS = [
    lambda req, res: print("REST api Python example 🐍")
]


@pytest.fixture
def http_method():
    """Returns a HttpMethod"""
    _router = router.Router()
    _method = 'GET'
    return httpmethod.HttpMethod(_router, _method, _router.route)


@pytest.mark.lib_router
@pytest.mark.parametrize("path", PATHS)
def test_default(http_method: httpmethod.HttpMethod, path):
    """we include a valid route and controllers"""
    _default = http_method.default(
        path,
        *CONTROLLERS
    )
    assert _default == http_method.router, "test failed"


@pytest.mark.lib_router
@pytest.mark.parametrize("path", PATHS)
def test_default_exception(http_method: httpmethod.HttpMethod, path):
    with pytest.raises(ValueError) as excinfo:
        # we don't include a valid route, because the handles aren't passed
        _default = http_method.default(
            path
        )
    assert "error: The route has the next format: METHOD(path, [...handlers functions])" == str(
        excinfo.value)


@pytest.mark.lib_router
@pytest.mark.parametrize("path", PATHS)
def test_default_type_error(http_method: httpmethod.HttpMethod, path):
    with pytest.raises(TypeError) as excinfo:
        # we don't include a valid path, because is necesary a string for the path
        _default = http_method.default(
            123,
            *CONTROLLERS
        )
    assert "error: The path type must be a string format" == str(
        excinfo.value
    )
