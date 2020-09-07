# Werkzeug
from werkzeug.serving import run_simple

# Environs
from environs import Env

# Retic
from retic.lib.router import Router

APP_HOSTNAME = "127.0.0.1"
APP_PORT = 1801


class App(object):
    def __init__(self, env):
        """
        Main instance of the application.

        :param env: Environment variables.
        """
        self.router: Router = None
        self.apps = {}
        self.env: Env = env
        self.config: Config = Config(env)

    @property
    def config(self):
        return self.__config

    @config.setter
    def config(self, value):
        """If the object exists you can't replace his value.

        Visit to documentation if you want clear the settings with the function
        ``app.config.clear()``

        Visit to documentation if you want set the settings from a onject with the funciont
        ``app.config.from_object()``
        """
        if hasattr(self, "config"):
            raise TypeError(
                "error: You can't assign the settings of this ways. if you want to assign from an object please use to *app.config.from_object()* function"
            )
        self.__config = value

    @property
    def router(self):
        return self.__router

    @router.setter
    def router(self, value):
        self.__router = value

    def application(self, environ, start_response):
        """Application for send the response returned by the application to the client

        :param environ: Request is used to describe an request to a server.
        :param start_response: Represents a response from a web request."""
        if not self.router:
            if environ.get('PATH_INFO') == '/':
                _status = '200 OK'
                _message = "Welcome to Retic!"
            else:
                _status = '404 Not found'
                _message = "error: The HTTP method {0} doesn't exist".format(
                    environ.get('REQUEST_METHOD')
                )
            start_response(_status, [('Content-Type', 'text/html')])
            return [_message.encode("utf8")]
        else:
            return self.router.main(environ, start_response)

    def clear(self):
        """Clear the App"""
        self.router: Router = None
        self.config.clear()
        self.apps.clear()

    def use(self, item: any, name: str = ""):
        """method of configuring the middleware.

        :param item: Item of specific type for specific settings in a app
        :param name: Name of the item to save
        """

        """TODO: implement another types of item"""
        if isinstance(item, Router):
            self.router = item
        elif name:
            self.apps.setdefault(name, item)
        else:
            raise KeyError("error: A name for the item is necesary")

    def listen(
        self,
        hostname: str = APP_HOSTNAME,
        port: int = APP_PORT,
        application: any = None,
        use_reloader: bool = False,
        use_debugger: bool = False,
        use_evalex: bool = True,
        extra_files: any = None,
        reloader_interval: int = 1,
        reloader_type: str = 'auto',
        threaded: bool = False,
        processes: int = 1,
        request_handler: any = None,
        static_files: any = None,
        passthrough_errors=False,
        ssl_context: any = None
    ):
        """Create a server based in settings parameters.

        :param hostname: The host to bind to, for example ``'localhost'``.
            If the value is a path that starts with ``unix://`` it will bind
            to a Unix socket instead of a TCP socket..
        :param port: The port for the server.  eg: ``8080``
        :param application: the WSGI application to execute
        :param use_reloader: should the server automatically restart the python
                            process if modules were changed?
        :param use_debugger: should the werkzeug debugging system be used?
        :param use_evalex: should the exception evaluation feature be enabled?
        :param extra_files: a list of files the reloader should watch
                            additionally to the modules.  For example configuration
                            files.
        :param reloader_interval: the interval for the reloader in seconds.
        :param reloader_type: the type of reloader to use.  The default is
                            auto detection.  Valid values are ``'stat'`` and
                            ``'watchdog'``. See :ref:`reloader` for more
                            information.
        :param threaded: should the process handle each request in a separate
                        thread?
        :param processes: if greater than 1 then handle each request in a new process
                        up to this maximum number of concurrent processes.
        :param request_handler: optional parameter that can be used to replace
                                the default one.  You can use this to replace it
                                with a different
                                :class:`~BaseHTTPServer.BaseHTTPRequestHandler`
                                subclass.
        :param static_files: a list or dict of paths for static files.  This works
                            exactly like :class:`SharedDataMiddleware`, it's actually
                            just wrapping the application in that middleware before
                            serving.
        :param passthrough_errors: set this to `True` to disable the error catching.
                                This means that the server will die on errors but
                                it can be useful to hook debuggers in (pdb etc.)
        :param ssl_context: an SSL context for the connection. Either an
                            :class:`ssl.SSLContext`, a tuple in the form
                            ``(cert_file, pkey_file)``, the string ``'adhoc'`` if
                            the server should automatically create one, or ``None``
                            to disable SSL (which is the default).
        source by: werkzeug.serving
        """

        """TODO: Welcome message after the server is created"""
        run_simple(
            hostname=hostname,
            port=int(port),
            application=application or self.application,
            use_reloader=use_reloader,
            use_debugger=use_debugger,
            use_evalex=use_evalex,
            extra_files=extra_files,
            reloader_interval=reloader_interval,
            reloader_type=reloader_type,
            threaded=threaded,
            processes=processes,
            request_handler=request_handler,
            static_files=static_files,
            passthrough_errors=passthrough_errors,
            ssl_context=ssl_context
        )


class Config(object):
    def __init__(self, env):
        """Variables from the environment"""
        self.env = env
        """variables from user settings"""
        self.config = {}

    @property
    def env(self):
        return self.__env

    @env.setter
    def env(self, value):
        self.__env = value

    @property
    def config(self):
        return self.__config

    @config.setter
    def config(self, value):
        """If the type of the value is not dict, it is not allowed"""
        if not isinstance(value, dict):
            raise TypeError(
                "error: A settings dictionary of type dict is necesary"
            )
        self.__config = value

    def get(self, key: str, default_value: dict = None, callback: any = None):
        """Returns the value of the parameter with the specified name.
        If the variable doesn't exist in the configuration values, this search
        in the environment variables and return a string. If you need a specific
        type of the environment variable, you need to use *app.env.int("variable_name")* for example.

        :param key: Name of the variable to find
        :param default_value: Value of the variable if this one doesn't exist
        :param callback: Function that is executed after getting the value
        """
        _value = self.__config.get(key, self.env(key, default_value))
        if not callback:
            return _value
        return callback(_value)

    def set(self, key: str, value: dict):
        """Set a value in the settings of the app.

        Please note that names are not case sensitive.

        :param key: Name of the variable to set
        :param value: Value of the variable
        """
        self.__config.setdefault(key, value)

    def from_object(self, settings: dict):
        """Set settings in based a dictionary, for example, if you want to
        set a additional configuration you nedd pass:

        ``app.config.from_object( { u'port': 8080 } )``

        :param settings: An object of type dictionary that contains the configurations
        """
        if not isinstance(settings, dict):
            raise TypeError(
                "error: A settings dictionary of type dict is necesary"
            )
        self.__config = {**self.__config, **settings}

    def clear(self):
        """Clear the actual settings, however, the settings from the environment 
        variables isn't clear. You can search variables in the environment with the function
        ``app.config.get("environment_name")``
        """
        self.__config.clear()
