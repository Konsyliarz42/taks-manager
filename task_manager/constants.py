from enum import Enum

PASSWORD_FIELD_LENGTH = {
    "min": 8,
    "max": 512,
}
STRING_FIELD_LENGTH = {
    "min": 4,
    "max": 256,
}


class HttpCodes(Enum):
    OK = 200
    CREATED = 201
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    NOT_FOUND = 404
