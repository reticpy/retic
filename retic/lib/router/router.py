from retic.lib.hooks.responses import Request, Response, Next
from retic.lib.translation.gettext import _s
from httpmethods import get_http_methods
from inspect import getfile
from .httpmethod import HttpMethod
from .route import Route
from .layer import Layer
import traceback
import sys
import os


class Router(object):
    def __init__(self):
        """Initial instance of the Router Class"""
        self.__dict__ = {
            key: HttpMethod(key, self.route).default for key in get_http_methods()
        }
        self.name = "router"
        self.methods = {key: [] for key in get_http_methods(True)}
        self.args = self.params = []
        self.result = None

    def main(self, environ: dict, start_response: dict):  # []
        """Router main for handle all routes

        :param environ: Request is used to describe an request to a server.
        :param start_response: Represents a response from a web request."""
        try:
            _request = Request(environ).config()
            _response = Response().config(environ, start_response, self._set_response)
            self._endpoint(_request, _response)
            _result = self.result
            self.result = None
            return _result
        except Exception as e:
            return Response(str(e))(environ, start_response)

    def route(self, path: str, method: str, handlers: list):  # Route
        """Create a Route instance and adds this route to specific controller
        of a HTTP method in a Router.

        :param path: Route to searching in the layer
        :param method: HTTP Request Method from the client request
        :param handlers: List of controllers functions from a routes files
        """
        _route = Route(path)
        for _handler in handlers:
            assert _handler, _s('NO_VALID_ROUTE')
            layer = Layer(
                "/",
                {
                    u"strict": False,
                    u"end": True
                },
                _handler
            )
            _route.stack.append(layer)
        _layer = Layer(
            path,
            {
                u"strict": False,
                u"end": True
            },
            _route.dispatch
        )
        _layer.route = _route
        self.methods[method].append(_layer)
        return _route

    def _set_response(self, item: dict):
        """Response function for the request."""
        if self.result:
            print(os.path.abspath(getfile(item)))
            print(_s('ERR_HTTP_HEADERS_SENT'))
            return
        self.result = item

    def _endpoint(self, req: Request, res: Response):  # []
        """This function handle any request from a client, search in the Route List

        :param req: Request is used to describe an request to a server.
        :param res: Represents a response from a web request."""
        try:
            _method = self.methods[req.method]
            if not _method:
                raise KeyError(_s('NO_VALID_METHOD {0}').format(req.method))

            _layer: Layer = self._search_layer(req.path, _method)

            if not _layer:
                raise KeyError(_s('NO_VALID_METHOD {0}').format(req.method))

            _has_method = self._handles_method(_layer)

            assert _has_method, _s('NO_VALID_ROUTE')

            req.params = _layer.params
            return _layer.handle_request(req, res, Next(req, res, _layer))
        except KeyError as e:
            return res.not_found(str(e))
        except Exception as e:
            traceback.print_exc(file=sys.stdout)
            return res.bad_request(str(e))

    def _search_layer(self, path: str, method: str):  # Layer
        """Search a specific Layer using a path and method.

        :param path: Route to searching in the layer
        :param method: HTTP Request Method from the client request
        :return: None if the layer doesn't exists, and a Layer Object
        if the layer is found."""
        _match = None
        for _layer in method:
            _match = _layer.match(path)
            if _match:
                break
        return _match

    def _handles_method(self, layer: Layer):
        """Check if the handle from the Layer is a controller function."""
        return True if layer.route.stack[0].handle else False
