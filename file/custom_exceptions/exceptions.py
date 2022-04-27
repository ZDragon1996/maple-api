from rest_framework.exceptions import APIException


class MaximumFileSizeException(APIException):
    status_code = 400
    default_detail = 'File size greater than 200MB is not supported. Feel free to contact @gmail.com for more info.'
    default_code = 'maximum_filesize'


class InvalidFileSizeException(APIException):
    status_code = 400
    default_detail = 'Invalid file for conversion. Feel free to contact @gmail.com for more info.'
    default_code = 'invalid_data'
