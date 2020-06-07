# Retic
from retic import cfg

# Gettext
import gettext

DOMAIN = cfg.APP_LANG_DOMAIN
LOCALEDIR = cfg.APP_LANG_LOCALEDIR
LANGUAGES = cfg.APP_LANG_LANGUAGES
FALLBACK = cfg.APP_LANG_FALLBACK
_t = None

if LOCALEDIR:
    _exists = gettext.find(DOMAIN, LOCALEDIR, LANGUAGES, all=False)
    if not _exists:
        raise FileNotFoundError(
            "{0} doesn't have a valid .mo translate file, check if you have a .po files"
        ).format(LOCALEDIR)

    t = gettext.translation(
        domain=DOMAIN,
        localedir=LOCALEDIR,
        languages=LANGUAGES,
        fallback=FALLBACK
    )
    _t = t.gettext
