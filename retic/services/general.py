# Repath
from repath import pattern

# Inspect
import inspect

# Re
import re


def _path_regexp(path, keys, options):
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


def _get_number_parameters(func):
    """Returns the number of parameters of a specific function."""
    return len(inspect.signature(func).parameters)


def _get_body_request(app_iter):
    """Generate a string from response of the app requests

    :param app_iter: Response from the request to api
    """
    return (b''.join(app_iter).splitlines()[0]).decode("utf-8")


def validate_obligate_fields(fields: any = None):
    """Validate if a list of obligate params are valid    

    :param fields: object that contains all params that are obligate, 
    these values can be arrays or simple values."""

    '''You can use the following example:

    _validate = validate_obligate_fields({     
        u'files': req.files.get("files", None)         
    })

    if _validate["valid"] is False:        
        return res.bad_request(            
            error_response_service(                
                "The param {} is necesary.".format(_validate["error"])                
            )            
        )
    '''
    if not fields:
        raise ValueError("error: A value for fields is necessary.")

    for field in fields:
        _item = fields.get(field, None)
        if _item == None \
                or (isinstance(_item, str) and _item == "") \
                or (isinstance(_item, list) and not _item):
            return {
                u'valid': False,
                u'error': field
            }
    return {
        u'valid': True,
        u'error': None
    }
