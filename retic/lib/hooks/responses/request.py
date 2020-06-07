# Werkzeug
from werkzeug.wrappers import Request

# Utils
from retic.utils.json import parse


class Request(Request):
    retic = {}
    params = {}
    """Initial instance of the Request Class"""

    def config(self):
        """Set another attributes to Instance"""
        self.body = self._get_body()
        return self

    def param(self, key: str, default_value: str = None):  # str
        """Returns the value of the parameter with the specified name.
        
        :param key: Name of the variable to set
        :param default_value: Value of the variable if this one doesn't exist
        """
        if key in self.params:
            return self.params.get(key)
        elif key in self.body:
            return self.body.get(key)
        elif key in self.args:
            return self.args.get(key)
        return self.retic.get(key, default_value)

    def set(self, key: str, value: any = None):  # str
        """Set a value in the requests (req).

        Please note that names are not case sensitive.
        
        :param key: Name of the variable to set
        :param value: Value of the variable
        """
        try:
            return self.retic.setdefault(key.lower(), value)
        except KeyError:
            return None

    def get(self, key: str):  # str
        """Returns the value of the request (req).

        Please note that names are not case sensitive.
        
        :param key: Name of the variable to find
        """
        try:
            return self.retic.get(key.lower(), None)
        except KeyError:
            return None

    def all_params(self):  # dict
        """Returns the value of all the parameters sent in the request,
        combined into a single dictionary.

        It includes parameters parsed from the URL path, the request body,
        and the query string, in that order."""
        return {**self.params, **self.body, **self.args, **self.retic}

    def _get_body(self):
        _content_type = self.headers.get('content-type', type=str)
        try:
            if _content_type.startswith('application/json'):
                _data = parse(self.get_data())
            elif _content_type.startswith('multipart/form-data') \
                    or _content_type.startswith('application/x-www-form-urlencoded'):
                _data = self.form
            else:
                _data = {u"body": self.get_data().decode('utf-8')}
            return _data
        except Exception as e:
            return {}
