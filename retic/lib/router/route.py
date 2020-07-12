# Utils
from retic.services.core.general import get_number_parameters


class Route(object):
    def __init__(self, path: str):
        """Initial instance of the Route Class

        :param path: Route to searching in the layer"""
        self.methods = None
        self.stack = []
        self.path = path

    def dispatch(self, req, res, next):  # function
        """Interface beetwen the *controller function** and **route**

        :param req: Request is used to describe an request to a server.
        :param res: Represents a response from a web request.
        :param next: It must call next() to pass control to the next middleware function
        """
        _handles = next.stack
        """Check if the next function exists"""
        if not _handles:
            return
        # assert _handles, "error: Next function is invalid, the function has not more controllers"

        _fn = _handles.pop(0).handle
        _num_param = get_number_parameters(_fn)

        if _num_param == 3:
            return _fn(req, res, next.next)
        elif _num_param == 2:
            return _fn(req, res)
        raise Exception("error: The controllers parameters are invalid")
