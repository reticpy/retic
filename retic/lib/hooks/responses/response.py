# Werkzeug
from werkzeug.wrappers import Response
from werkzeug.routing import RequestRedirect

# Httpmethods
from httpmethods import get_status_by_code

# Utils
from retic.services.general.json import jsonify


class Response(Response):

    def _config(
        self,
        environ,
        start_response,
        set_response
    ):
        """Config instance of the Responses Class

        :param environ: Represents a request from a web request.
        :param start_response: Represents a response from a web request.
        :param set_response: Response function for the request.
        """
        self._environ = environ
        self._start_response = start_response
        self._set_response = set_response
        # set default headers
        self.set_headers('content-type', "application/json")
        return self

    def bad_request(self, content: any = ""):  # Response
        """This method response a *400 Bad Request* response to the client,
        this indicate that the request is invalid.

        This generally means that the request contained invalid parameters
        or headers, or that you tried to do something that your application
        logic does not support.

        :param content: Information to send the client, a message, a dict, etc.
        If it doesn't exist, it sends a status message from the status code.
        """
        return self._send_by_status(400, content)

    def forbidden(self, content: any = ""):  # Response
        """This method is used to send a *403 Forbidden* response to the client,
        indicating that a request is not authorized.

        This generally means that the user agent tried to do something that they
        were not authorized to do, such as changing another user's password.

        :param content: Information to send the client, a message, a dict, etc.
        If it doesn't exist, it sends a status message from the status code.
        """
        return self._send_by_status(403, content)

    def not_found(self, content: any = ""):  # Response
        """This method is used to send a *404 Not found* response.

        When called manually from your application code, this method is normally used to
        indicate that the user agent tried to find, update, or delete something that doesn't exist.

        :param content: Information to send the client, a message, a dict, etc.
        If it doesn't exist, it sends a status message from the status code.
        """
        return self._send_by_status(404, content)

    def ok(self, content: dict = None):  # Response
        """This method is used to send a *200 OK* response to the client.

        :param content: Information to send the client, a message, a dict, etc.
        If it doesn't exist, it sends a status message from the status code.
        """
        return self._send_by_status(200, content)

    def server_error(self, content: any = ""):
        """This method is used to send a *500 Server Error* response to the client,
        indicating that some kind of server error occurred.

        :param content: Information to send the client, a message, a dict, etc.
        If it doesn't exist, it sends a status message from the status code.
        """
        return self._send_by_status(500, content)

    def send(self, content: any = None):  # Response
        """Send a string response in a non-JSON format (XML, CSV, plain text, etc.).

        This method is used in the underlying implementation of most other terminal response methods.

        :param content: Information to send the client, a message, a dict, etc.
        If it doesn't exist, it sends a status message from the status code.
        """
        return self._send_string(content if content else {})

    def set_headers(self, headers: dict, value: str = None):  # self
        """Sets the specified response header to the specified value.

        Alternatively, you can pass a single object argument (headers)
        to set multiple header fields at once, where the keys are the names
        of the header fields and the corresponding values ​​are the desired values.

        :param headers: It can be of type ``dict``, to represent a headers object 
        that are added to the current headers. If it is of type ``str`` it will 
        be used to access a specific header. Any other format may cause an error exception.

        :param value: Value to assign to the specified header. By default it has a 
        value of ``None``.
        """
        if type(headers) is dict and value is None:
            self.headers = {**self.headers, **headers}
        elif type(headers) is str:
            self.headers[headers] = value
        else:
            raise TypeError(
                "error: Headers have an invalid type. You can use dict or str."
            )
        return self

    def set_status(self, code: int):  # self
        """Set the status code for this response.

        :param code: Number representing the status code of the HTTP response
        """
        self.status_code = code
        return self

    def redirect(self, new_url: str):  # Response
        """Redirect to another url with the actual request
        
        :param new_url: URL to redirect.
        """
        _result = RequestRedirect(new_url=new_url).get_response(self._environ)
        return self._set_response(_result(self._environ, self._start_response))

    def _send_string(self, content: str = ""):  # Response
        """Send a response to http requests.

        :param content: Information to send the client, a message, a dict, etc.
        If it doesn't exist, it sends a status message from the status code.
        """
        self.set_data(jsonify(content))
        return self._set_response(self(self._environ, self._start_response))

    def _send_by_status(self, status, content):
        return self.set_status(status)._send_string(content or get_status_by_code(status))

    def favicon(self, req, res):
        return self.ok()
