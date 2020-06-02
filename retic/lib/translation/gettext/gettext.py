from retic import cfg
import gettext

DOMAIN = cfg.APP_LANG_DOMAIN
LOCALEDIR = cfg.APP_LANG_LOCALEDIR
LANGUAGES = cfg.APP_LANG_LANGUAGES
FALLBACK = cfg.APP_LANG_FALLBACK
_s = _t = None

core = gettext.translation(
    "base", "retic/locale",
    languages=["en_US"],
    fallback=True
)
_s = core.gettext

if LOCALEDIR:
    _exists = gettext.find(DOMAIN, LOCALEDIR, LANGUAGES, all=False)
    if not _exists:
        raise FileNotFoundError(_s("ERR_NOT_LOCALE {0}").format(LOCALEDIR))

    t = gettext.translation(
        domain=DOMAIN,
        localedir=LOCALEDIR,
        languages=LANGUAGES,
        fallback=FALLBACK
    )
    _t = t.gettext
