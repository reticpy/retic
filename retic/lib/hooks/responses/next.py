class Next(object):
    def __init__(self, req: any, res: any, layer: any):
        """Initial instance of the Next Class

        :param req: Request is used to describe an request to a server.
        :param res: Represents a response from a web request.
        :param layer: Layer that contains a route instance for a specific path
        """
        self.layer = layer
        self.stack = layer.route.stack.copy()
        self.req = req
        self.res = res

    def next(self):
        """It must call next() to pass control to the next middleware function"""
        self.layer.handle_request(self.req, self.res, self)
