from retic.lib.hooks.system.env import env

APP_LANG_LOCALEDIR = env("APP_LANG_LOCALEDIR", None)
APP_LANG_DOMAIN = env.str("APP_LANG_DOMAIN", "base")
APP_LANG_LANGUAGES = env.list("APP_LANG_LANGUAGES", ["en_US"])
APP_LANG_FALLBACK = env.bool("APP_LANG_FALLBACK", True)
