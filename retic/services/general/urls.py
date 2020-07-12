# Re
import re

# Urllib
import urllib.parse

# Unicodedata
import unicodedata


def urlencode(url: str):
    """This function is convenient when encoding a string to 
    use in a query part of a URL, as a convenient way to pass 
    variables to the next page.

    :param url: URL to encode.
    """
    key = urllib.parse.quote_plus(url)
    return key


def slugify(text: str = ""):
    """Simplifies ugly strings into something URL-friendly.

    :param text: Text to simplifies in ``str`` type    
    """
    # Reference: https://github.com/mikaelho/docgen/blob/master/docgen.py
    # "[Some] _ Article's Title--"
    # "[some] _ article's title--"
    text = str(text).lower()
    # "[some] _ article's_title--"
    # "[some]___article's_title__"
    for c in [' ', '-', '.', '/']:
        text = text.replace(c, '_')
    # "[some]___article's_title__"
    # "some___articles_title__"
    text = re.sub('\W', '', text)
    # "some___articles_title__"
    # "some   articles title  "
    text = text.replace('_', ' ')

    # "some   articles title  "
    # "some articles title "
    text = re.sub('\s+', ' ', text)

    # "some articles title "
    # "some articles title"
    text = text.strip()

    # "some articles title"
    # "some-articles-title"
    text = text.replace(' ', '-')
    # delete acents
    text = unicodedata.normalize("NFD", text)
    text = text.encode("utf8").decode("ascii", "ignore")
    text = urlencode(text)
    return text
