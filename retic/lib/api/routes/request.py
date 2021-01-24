# Werkzeug
from werkzeug.wrappers import Request

# Utils
from retic.services.general.json import parse


class Body(object):
    """Class for the body from a request"""

    def __init__(self, type: dict, value: dict):
        """Define the type of the object"""
        self.type: dict = type
        """Value of the object"""
        self.value: dict = value

    @property
    def type(self):
        return self.__type

    @type.setter
    def type(self, value):
        self.__type = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value


class Request(Request):
    """Initial instance of the Request Class"""

    @property
    def retic(self):
        return self.__retic

    @retic.setter
    def retic(self, value):
        if hasattr(self, "retic"):
            raise TypeError(
                "error: You can't assign the settings of this ways. if you want to assign from an object please use to *req.retic.clear()* function"
            )
        self.__retic = value

    def _config(self):
        """Set another attributes to Instance"""
        self.body: Body = self._get_body()
        self.retic = self.params = {}
        return self

    def param(self, key: str, default_value: any = None, callback=None):
        """Returns the value of the parameter with the specified name.

        req.param(...) finds in the URL path, body, and query string (in that order) 
        for the specified parameter. If no parameter value exists anywhere in the 
        request with the given name, it returns None or the optional default value if specified.

        :param key: Name of the parameter to find
        :param default_value: Value of the parameter if this one doesn't exist
        :param callback: Function that is executed after getting the value        
        """
        if key in self.params:
            _value = self.params.get(key)
        elif key in self.body.value:
            _value = self.body.value.get(key)
        else:
            _value = self.args.get(key, default_value)
        if not _value and default_value:
            _value = default_value
        if not callback:
            return _value
        return callback(_value)

    def set(self, key: str, value: any = None):
        """Set a value in the requests (req).

        Please note that names are not case sensitive.

        :param key: Name of the variable to set
        :param value: Value of the variable
        """
        return self.retic.setdefault(key.lower(), value)

    def get(self, key: str, default_value: any = None):
        """Returns the value of an object in retic with a specific name. 
        Please note that names are not case sensitive. 

        If the value does not exist in the request, it returns None or 
        the default value specified by default.

        :param key: Name of the variable to find
        :param default_value: Value of the parameter if this one doesn't exist
        """
        return self.retic.get(key.lower(), default_value)

    def all_params(self):
        """Returns the value of all the parameters sent in the request,
        combined into a single dictionary.

        It includes parameters parsed from the URL path, the request body,
        and the query string, retic dict in that order."""
        return {**self.params, **self.body.value, **self.args, **self.retic}

    def _get_body(self):
        """Get the body for a request from to client. If this one is not exists, return

        ``{ type: "undefiend", value: "undefiend" }``

        The response takes possibly four keys: json, form, text, and raw. 

        For example if the request body is a json object, you will get:

        ``{ type: "json", value: json_object }``

        Also, if a exception is detected, you will get

        ``{ type: "error", value: error_object }``
        """
        _type = ''
        _value = ''
        _content_type = self.headers.get('content-type', type=str)
        try:
            if not _content_type:
                _type = 'undefiend'
                _value = 'undefiend'
            elif _content_type.startswith('application/json'):
                _type = "json"
                _value = parse(self.get_data())
            elif _content_type.startswith('multipart/form-data') \
                    or _content_type.startswith('application/x-www-form-urlencoded'):
                _type = 'form'
                _value = self.form
            elif _content_type.startswith('text/'):
                _type = "text"
                _value = self.get_data().decode("utf-8")
            else:
                _type = 'raw'
                _value = self.get_data()
            return Body(
                type=_type,
                value=_value,
            )
        except Exception as e:
            return Body(
                type='error',
                value=e,
            )
