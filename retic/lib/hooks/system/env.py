# Environs
from environs import Env

# Utils
import retic.services.core.msgfmt as msgfmt

env = Env()
env.read_env()

# TODO: Implement gettext libs
def build_api(env):
    # load files
    msgfmt.make("retic\locale", "base")
    _locale = env("APP_LANG_LOCALEDIR", None)
    if not _locale:
        return
    msgfmt.make(_locale, env.str("APP_LANG_DOMAIN", "base"))


# build_api(env)
