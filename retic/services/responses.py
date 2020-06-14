"""Standard responses to client"""

def error_response_service(msg=""):
    """Define a error json response to send a client"""
    _data_response = {
        u'valid': False,
        u'msg': msg
    }
    return _data_response


def success_response_service(data=None, msg=""):
    """Define a success json response to send a client"""
    _data_response = {
        u'valid': True,
        u'msg': msg,
        u'data': data
    }
    if not data:
        del _data_response["data"]
    return _data_response
