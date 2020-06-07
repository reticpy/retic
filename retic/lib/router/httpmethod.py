from retic.utils.exceptions import get_file_error_exception
import traceback
import sys


class HttpMethod(object):
    def __init__(self, method: str, route: any):
        """Initial instance of the HttpMethod Class.

        :param method: HTTP Request Method from the client request
        :param route: Route function from Router class
        """
        self.method = method
        self.route = route

    def default(self, *args):  # self
        """Create a new route in base a path and controllers from the routes config

        :param method: HTTP Request Method from the client request
        :param route: Route function from Router class
        """
        try:
            if len(args) < 2:
                raise Exception(
                    "error: The route has the next format: METHOD(path, [...handlers functions])"
                )
            path = args[0]
            if type(path) is not str:
                raise TypeError("error: The path type must be a string format")
            self.route(path, self.method.upper(), args[1:])
            return self
        except Exception as e:
            traceback.print_exc(file=sys.stdout)
            print(get_file_error_exception())
            sys.exit(0)
