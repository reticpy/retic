# Pytest
import pytest

# Retic
from retic import App as app


@pytest.mark.lib
def test_config_attribute():
    """Clear the configuration"""
    app.config.clear()
    """Check that the variables aren't exists"""
    assert app.config.get("APP_LANG") == None
    assert app.config.get("APP_HOST") == None
    """we include a basic setting to app"""
    app.config.set("APP_LANG", "en_US")
    app.config.set("APP_HOST", "localhost")
    """Check if this value was saved in the object"""
    assert app.config.get("APP_LANG") == "en_US", \
        "The value from the configuration item is different to value saved"
    assert app.config.get("APP_HOST") == "localhost", \
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
