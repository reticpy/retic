from .exceptions import get_file_error_exception
from json import dumps, loads


def jsonify(object):
    """Convert a object to a JSON string."""
    try:
        return dumps(object)
    except Exception as e:
        return dumps({
            u"path": get_file_error_exception(3),
            u"error": str(e)
        })


def parse(str):
    """Deserialize (a str, bytes, or bytearray instance that contains 
    a JSON document) to a Python object.
    """
    return loads(str)
