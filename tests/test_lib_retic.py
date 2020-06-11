# Pytest
import pytest

# Retic
from retic import App as app


@pytest.mark.lib
def test_config_attribute():
    """we include a basic setting to app and check if this value was saved in the object"""
    app.config.set("APP_LANG", "en_US")
    app.config.set("APP_HOST", "localhost")
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
