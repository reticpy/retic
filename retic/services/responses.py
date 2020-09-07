"""Standard responses to client"""


def error_response(msg: str = ""):
    """Define a error json response to send a client.

    :param msg: A message indicating that the request has errors.
    """
    _data_response = {
        u'valid': False,
        u'msg': msg
    }
    return _data_response


def success_response(data: any = None, msg: str = ""):
    """Defines the structure of a response to a client request in JSON format.

    :param data: Information to send to client.
    :param msg: A message indicating that the request completed successfully.
    """
    _data_response = {
        u'valid': True,
        u'msg': msg,
        u'data': data
    }
    return _data_response
