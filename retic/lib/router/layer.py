from retic.utils.exceptions import get_file_error_exception
from retic.lib.translation.gettext import _s
from retic.utils.general import path_regexp


class Layer(object):
    def __init__(self, path: str, options: dict, fn: any):
        """Initial instance of the Layer Class

        :param path: Route to searching in the layer
        :param options: Options for the regexp expression
        :param fn: Route dispatch function for the request"""
        self.handle = fn
        self.keys = []
        self.name = fn.__name__ if fn.__name__ else '<anonymous>'
        self.params = self.path = self.route = None
        self.regexp = path_regexp(path, self.keys, options)

    def handle_request(self, req, res, next):  # dispatch
        """Return a handle request for specific route"""
        try:
            return self.handle(req, res, next)
        except Exception as e:
            get_file_error_exception(3)
            raise RuntimeError(_s('NO_VALID_CONTROLLERS {0}').format(str(e)))

    def match(self, path: str):  # self
        """Search to specific layer for a path

        :param path: Route to searching in the layer
        :return: Specific layer that was matched with the path"""
        _match = self.regexp.match(path)
        if not _match:
            self.path = self.params = None
            return None
        self.path = _match.string
        self.params = _match.groupdict()
        return self
