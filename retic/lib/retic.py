from werkzeug.serving import run_simple
from retic.lib.translation.gettext import _s
from .router import Router

APP_HOST = "0.0.0.0"
APP_PORT = 1801


class App(object):
    def __init__(self):
        self.router = None
        self.apps = {}

    def application(self, environ, start_response):
        """Application for send the response returned by the application to the client

        :param environ: Request is used to describe an request to a server.
        :param start_response: Represents a response from a web request."""
        if not self.router:
            start_response('200 OK', [('Content-Type', 'text/html')])
            return [_s("DEFAULT_RESPONSE").encode("utf8")]
        else:
            return self.router.main(environ, start_response)

    def use(self, item: any, name: str = ""):
        """method of configuring the middleware.

        :param item: item of specific type for specific settings in a app
        :return: instance of the parant type for the item
        """ 

        """TODO: implement another types of item"""
        if isinstance(item, Router):
            self.router = item
        elif name:
            self.apps.setdefault(name, item)

    def listen(
        self,
        hostname=APP_HOST,
        port=APP_PORT,
        application=None,
        use_reloader=False,
        use_debugger=False,
        use_evalex=True,
        extra_files=None,
        reloader_interval=1,
        reloader_type='auto',
        threaded=False,
        processes=1,
        request_handler=None,
        static_files=None,
        passthrough_errors=False,
        ssl_context=None
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
