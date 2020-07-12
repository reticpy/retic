# Repath
from repath import pattern

# Inspect
import inspect

# Re
import re


def path_regexp(path, keys, options):
    """ Return a regular expression function for a specific route

    :param path: Route to searching in the layer    
    :param keys: List of keys from the route
    :param options: Options for the regexp expression    
    :return: A regular expression pattern string
    """
    _reg_exp = re.compile(pattern(path, **options))
    for _key in _reg_exp.groupindex:
        keys.append({
            u"name": _key,
            u"optional": False
        })
    return _reg_exp


def get_number_parameters(func):
    """Returns the number of parameters of a specific function."""
    return len(inspect.signature(func).parameters)


def get_body_request(app_iter):
    """Generate a string from response of the app requests

    :param app_iter: Response from the request to api
    """
    return (b''.join(app_iter).splitlines()[0]).decode("utf-8")