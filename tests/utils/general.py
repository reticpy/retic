def get_body_request(app_iter):
    """Generate a string from response of the app requests

    :param app_iter: Response from the request to api
    """
    return (b''.join(app_iter).splitlines()[0]).decode("utf-8")
