from werkzeug.wrappers import Response
from httpmethods import get_status_by_code
from retic.utils.json import jsonify


class Response(Response):

    def config(
        self,
        environ,
        start_response,
        set_response
    ):
        """Config instance of the Responses Class

        :param environ: Represents a request from a web request.
        :param start_response: Represents a response from a web request.
        :param set_response: Response function for the request."""
        self._environ = environ
        self._start_response = start_response
        self._set_response = set_response
        # set default headers
        self.set_headers('content-type', "application/json")
        return self

    def bad_request(self, content=""):  # Response
        """This method response a *400 Bad Request* response to the client,
        this indicate that the request is invalid.

        This generally means that the request contained invalid parameters
        or headers, or that you tried to do something that your application
        logic does not support."""
        return self._send_by_status(400, content)

    def forbidden(self, content=""):  # Response
        """This method is used to send a *403 Forbidden* response to the client,
        indicating that a request is not authorized.

        This generally means that the user agent tried to do something that they
        were not authorized to do, such as changing another user's password."""
        return self._send_by_status(403, content)

    def not_found(self, content=""):  # Response
        """This method is used to send a *404 Not found* response.

        When called manually from your application code, this method is normally used to
        indicate that the user agent tried to find, update, or delete something that doesn't exist."""
        return self._send_by_status(404, content)

    def ok(self, data: dict = None):  # Response
        """This method is used to send a *200 OK* response to the client."""
        return self._send_by_status(200, jsonify(data) if data else None)

    def server_error(self, content=""):
        """This method is used to send a *500 Server Error* response to the client,
        indicating that some kind of server error occurred."""
        return self._send_by_status(500, content)

    def send(self, data: dict = None):  # Response
        """Send a string response in a non-JSON format (XML, CSV, plain text, etc.).

        This method is used in the underlying implementation of most other terminal response methods."""
        return self.send_string(jsonify(data) if data else {})

    def set_headers(self, headers: dict, value: str = None):  # self
        """Sets the specified response header to the specified value.

        Alternatively, you can pass a single object argument (headers)
        to set multiple header fields at once, where the keys are the names
        of the header fields and the corresponding values ​​are the desired values."""
        if not value and type(headers) is dict:
            self.headers = {**self.headers, **headers}
        else:
            self.headers[headers] = value
        return self

    def set_status(self, code: int):  # self
        """Set the status code for this response."""
        self.status_code = code
        return self

    def send_string(self, data_str: str = ""):  # Response
        """Send a response to http requests"""
        self.set_data(data_str)
        self._set_response(self(self._environ, self._start_response))

    def _send_by_status(self, status, content):
        return self.set_status(status).send_string(content or get_status_by_code(status))

    def favicon(self, req, res):
        return self.ok()
