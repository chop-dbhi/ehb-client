

class ErrorConstants(object):
    ERROR_UNKNOWN = 0
    ERROR_RECORD_ID_NOT_FOUND = 1
    ERROR_FIELD_REQUIRED = 2
    ERROR_SUBJECT_ORG_ID_EXISTS = 3
    ERROR_INVALID_DATE_FORMAT = 4
    ERROR_EXTERNAL_SYSTEM_NAME_EXISTS = 5
    ERROR_RECORD_ID_ALREADY_IN_EXTERNAL_SYSTEM = 6
    ERROR_INVALID_CHOICE = 7
    ERROR_INVALID_QUERY = 8
    ERROR_NO_RECORD_FOUND_FOR_QUERY = 9
    ERROR_EXTERNAL_SYSTEM_URL_EXISTS = 10
    ERROR_ORGANIZATION_NAME_EXISTS = 11
    ERROR_GROUP_NAME_EXISTS = 12
    ERROR_ID_NOT_FOUND = 13
    ERROR_SUBJECT_ID_NOT_VALID = 14


class PageNotFound(Exception):
    def __init__(self, path):
        self.path = path
        self.errmsg = 'Page not found: ' + path


class ServerError(Exception):
    def __init__(self):
        self.errmsg = 'Error at server'


class MalformedRequestBody(Exception):
    def __init__(self, body):
        self.errmsg = 'Malformed request body: ' + body


class NotAuthorized(Exception):
    def __init__(self):
        self.errmsg = 'Not authorized for this request'


class InvalidArguments(Exception):
    def __init__(self, requiredArgs):
        self.errmsg = 'The method requires the following kwargs: ' + requiredArgs


class RequestedRangeNotSatisfiable(Exception):
    def __init__(self, given_range):
        self.errmsg = 'The range : ' + str(given_range) + ', was not found.'
