from os import stat
from rest_framework import status
from rest_framework.response import Response
from file.custom_exceptions.exceptions import MaximumFileSizeException, InvalidFileSizeException


def handle_invalid_file(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except:
            raise InvalidFileSizeException()

    return wrapper


def handle_max_size_file(func):
    def wrapper(*args, **kwargs):
        try:
            res = func(*args, **kwargs)
            return res
        except:
            raise MaximumFileSizeException()
    return wrapper
