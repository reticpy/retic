import inspect
import os


def get_file_error_exception(position=2):
    """Returns a file path of a file that created an invocation function"""
    _calframe = inspect.getouterframes(inspect.currentframe(), 2)
    return os.path.abspath(inspect.getfile(_calframe[position][0]))
