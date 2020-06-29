# Traceback
import traceback

# Sys
import sys

# Utils
from retic.services.exceptions import get_file_error_exception


class HttpMethod(object):
    def __init__(self, router, method: str, route: any):
        """Initial instance of the HttpMethod Class.

        :param router: Instance of the Router Class, this is use when I
            need to use router.get(...).get(...).post(...)
        :param method: HTTP Request Method from the client request
        :param route: Route function from Router class
        """
        self.router = router
        self.method = method
        self.route = route

    def default(self, *args):  # self
        """Create a new route in base a path and controllers from the routes config

        :param method: HTTP Request Method from the client request
        :param route: Route function from Router class
        """
        if len(args) < 2:
            raise ValueError(
                "error: The route has the next format: METHOD(path, [...handlers functions])"
            )
        path = args[0]
        if type(path) is not str:
            raise TypeError("error: The path type must be a string format")
        self.route(path, self.method.upper(), args[1:])
        return self.router
