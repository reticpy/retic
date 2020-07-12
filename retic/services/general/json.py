# Json
from json import dumps, loads

# Retic
from retic.services.exceptions import get_file_error_exception


def jsonify(object: any):
    """Convert a object to a JSON string.

    :param object: is the client response object, if the object is str, 
    it returns this value, otherwise it creates a jsonify of the object
    """
    try:
        # if is none, return a empty string
        if not object:
            return ""
        # if is a bytesm return the same value
        elif isinstance(object, bytes):
            return object
        # if is a string, return the same value
        elif isinstance(object, str):
            return object
        # return the value in string format
        elif isinstance(object, dict):
            return dumps(object)
        # return a error message
        else:
            raise "error: The format of the object for the response is invalid."
    except Exception as e:
        return dumps({
            u"path": get_file_error_exception(3),
            u"error": str(e)
        })


def parse(content: str):
    """Deserialize (a str, bytes, or bytearray instance that contains 
    a JSON document) to a Python object.

    :param content: Content of type str, bytes, or bytearray that contains a valid JSON.
    """
    return loads(content)
