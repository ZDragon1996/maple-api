from rest_framework import status
from rest_framework.response import Response


def handle_invalid_file(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    return wrapper
