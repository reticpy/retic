METHODS = 'GET,POST,DELETE,PUT,OPTIONS'
HAS_CREDENTIALS = True
ORIGIN = "*"
HEADERS = "Content-Type"
EXPOSE_HEADERS = "Content-Type"


def cors(
    methods: str = METHODS,
    has_credentials: bool = HAS_CREDENTIALS,
    origin: str = ORIGIN,
    headers: str = HEADERS,
    expose_headers: str = EXPOSE_HEADERS
):
    """CORS is an abbreviation that stands for 'Cross-Origin Resource 
    Sharing' and, as the name implies, allows sharing of resources 
    from a variety of sources.

    A simple cross-origin request would be when domain1.com would be 
    accessing a resource from domain2.com (the resource is an image, 
    a CSS file, or something else). This has some massive security 
    implications, of course, and the built-in behavior for browsers 
    is that they would restrict the cross-origin HTTP request.

    :param methods: The Access-Control-Allow-Methods response header indicates 
    which HTTP methods are allowed on a particular endpoint for cross-origin requests.
    :param has_credentials: Access-Control-Allow-Credentials response header tells 
    the browser that the server allows 
    credentials for a cross-origin request.
    :param origin: The Access-Control-Allow-Origin response header indicates 
    whether the resources in the response can be shared with the given origin.
    :param headers: The Access-Control-Allow-Headers response header is used 
    in response to a preflight request that includes the Access-Control-Request-Headers 
    to indicate which HTTP headers can be used during the actual request
    :param expose_headers: The Access-Control-Expose-Headers response header indicates 
    which headers can be exposed as part of the response by listing

    ``from retic import Router``

    ``router = Router()``

    ``router.use(cors())``
    """

    def set_middleware(req, res, next):
        """Set all cors headers in a response to Client.

        :param req: Request is used to describe an request to a server.
        :param res: Represents a response from a web request.
        :param next: It must call next() to pass control to the next middleware function
        """

        res.set_headers('Access-Control-Allow-Methods', has_credentials)
        res.set_headers('Access-Control-Allow-Credentials', methods)
        res.set_headers('Access-Control-Allow-Origin', origin)
        res.set_headers('Access-Control-Allow-Headers', headers)
        res.set_headers('Access-Control-Expose-Headers', expose_headers)
        next()
    return set_middleware
