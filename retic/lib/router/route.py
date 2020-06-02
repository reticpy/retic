from retic.utils.general import get_number_parameters
from retic.lib.translation.gettext import _s


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
        assert _handles, _s('ERR_DISPATCH_NEXT')
        
        _fn = _handles.pop(0).handle
        _num_param = get_number_parameters(_fn)
        
        if _num_param == 3:
            return _fn(req, res, next.next)
        elif _num_param == 2:
            return _fn(req, res)
        raise Exception(_s('ERR_CONTROLLER_FUNC'))
