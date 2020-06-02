from repath import pattern
import inspect
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
