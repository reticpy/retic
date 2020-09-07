# Werkzeug
from werkzeug.routing import RequestRedirect

# Httpmethods
from httpmethods import get_http_methods

# Inspect
from inspect import getfile

# Traceback
import traceback

# Sys
import sys

# Os
import os

# Retic
from retic.lib.api.routes import Request, Response, Next
from retic.lib.router.httpmethod import HttpMethod
from retic.lib.router.route import Route
from retic.lib.router.layer import Layer


class Router(object):
    def __init__(self, strict_slashes: bool = True):
        """Initial instance of the Router Class

        :param strict_slashe: If a rule ends with a forward slash but the matching URL does not, redirect to the ending no forward slash URL.
        """
        self.__dict__ = {
            key: HttpMethod(self, key, self.route).default for key in get_http_methods()
        }
        self.name = "router"
        self.methods = {key: [] for key in get_http_methods(True)}
        self.args = self.params = []
        self.result = None
        self.rules = {
            "strict_slashes": strict_slashes
        }
        self.middlewares = []

    @property
    def middlewares(self):
        return self.__middlewares

    @middlewares.setter
    def middlewares(self, value):
        self.__middlewares = value

    @property
    def result(self):
        return self.__result

    @result.setter
    def result(self, value):
        self.__result = value

    def main(self, environ: dict, start_response: dict):  # []
        """Router main for handle all routes

        :param environ: Request is used to describe an request to a server.
        :param start_response: Represents a response from a web request."""
        try:
            _request = Request(environ)._config()
            _response = Response()._config(environ, start_response, self._set_response)
            self._endpoint(_request, _response)
            _result = self._response_request(_response, self.result)
            self.result = None
            return _result
        except Exception as e:
            return Response(str(e))(environ, start_response)

    def use(self, fn):
        """Use to add a middleware that is execute for all routes

        :param fn: Route dispatch function for the request
        """
        """Set middle to routes"""
        self.middlewares.append(
            self._set_handler_to_layer(fn)
        )

    def route(self, path: str, method: str, handlers: list):  # Route
        """Create a Route instance and adds this route to specific controller
        of a HTTP method in a Router.

        :param path: Route to searching in the layer
        :param method: HTTP Request Method from the client request
        :param handlers: List of controllers functions from a routes files
        """
        _route = Route(path)
        for _handler in handlers:
            """Set handler to route"""
            _route.stack.append(
                self._set_handler_to_layer(_handler)
            )
        _layer = Layer(
            path,
            {
                u"strict": self.rules.get('strict_slashes', False),
                u"end": True
            },
            _route.dispatch
        )
        _layer.route = _route
        self.methods[method].append(_layer)
        return _route

    def _set_handler_to_layer(self, handler):
        assert handler, "error: The route has the next format: METHOD(path, [...handlers functions])"
        assert callable(
            handler), "error: The handler or middleware is not a valid function"
        _layer = Layer(
            "/",
            {
                u"strict": False,
                u"end": True
            },
            handler
        )
        return _layer

    def _set_response(self, item: dict):
        """Response function for the request."""
        self.result = item
        return self.result

    def _response_request(self, res, result):
        """Response to a client request. If response was not specific, return
        status 200 and message 200 for default

        :param res: Represents a response from a web request.
        :param result: Instance of the object with the werkzeug response
        """
        if result:
            return result
        return res.ok()

    def _endpoint(self, req: Request, res: Response):  # []
        """This function handle any request from a client, search in the Route List

        :param req: Request is used to describe an request to a server.
        :param res: Represents a response from a web request."""
        try:
            # validate if path contains slash and it isn't a "/" path
            if self.rules.get('strict_slashes', False) \
                    and len(req.path) > 1 \
                    and "/" in req.path[-1]:
                raise ValueError(req.path[:-1])

            # search the specific method
            _method = self.methods[req.method]
            if not _method:
                raise KeyError(
                    "error: The HTTP method {0} doesn't exist".format(
                        req.method)
                )

            # search the layer for this method
            _layer: Layer = self._search_layer(req.path, _method)

            if not _layer:
                raise KeyError(
                    "error: The HTTP method {0} doesn't exist".format(
                        req.method)
                )

            # search the first handle for this one
            _has_method = self._handles_method(_layer)

            assert _has_method, "error: The route has the next format: METHOD(path, [...handlers functions])"

            # set the params to request
            req.params = _layer.params
            # return the handle logic
            return _layer.handle_request(req, res, Next(req, res, _layer, self.middlewares))
        except ValueError as e:
            return res.redirect(str(e))
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
