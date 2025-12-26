class SendwithusError(Exception):
    """class representing Generic Http error."""

    def __init__(self, message=None, response=None):
        super().__init__(message)
        self.message = message
        self.response = response


class SendwithusBackoffError(SendwithusError):
    """class representing backoff error handling."""
    pass


class SendwithusBadRequestError(SendwithusError):
    """class representing 400 status code."""
    pass


class SendwithusUnauthorizedError(SendwithusError):
    """class representing 401 status code."""
    pass


class SendwithusForbiddenError(SendwithusError):
    """class representing 403 status code."""
    pass


class SendwithusNotFoundError(SendwithusError):
    """class representing 404 status code."""
    pass


class SendwithusConflictError(SendwithusError):
    """class representing 409 status code."""
    pass


class SendwithusUnprocessableEntityError(SendwithusError):
    """class representing 422 status code."""
    pass


class SendwithusRateLimitError(SendwithusBackoffError):
    """class representing 429 status code."""
    pass


class SendwithusInternalServerError(SendwithusBackoffError):
    """class representing 500 status code."""
    pass


class SendwithusNotImplementedError(SendwithusBackoffError):
    """class representing 501 status code."""
    pass


class SendwithusBadGatewayError(SendwithusBackoffError):
    """class representing 502 status code."""
    pass


class SendwithusServiceUnavailableError(SendwithusBackoffError):
    """class representing 503 status code."""
    pass


ERROR_CODE_EXCEPTION_MAPPING = {
    400: {
        "raise_exception": SendwithusBadRequestError,
        "message": "A validation exception has occurred."
    },
    401: {
        "raise_exception": SendwithusUnauthorizedError,
        "message": "The access token provided is expired, revoked, malformed or invalid for other reasons."
    },
    403: {
        "raise_exception": SendwithusForbiddenError,
        "message": "You are missing the following required scopes: read"
    },
    404: {
        "raise_exception": SendwithusNotFoundError,
        "message": "The resource you have specified cannot be found."
    },
    409: {
        "raise_exception": SendwithusConflictError,
        "message": "The API request cannot be completed because the requested operation would conflict with an existing item."
    },
    422: {
        "raise_exception": SendwithusUnprocessableEntityError,
        "message": "The request content itself is not processable by the server."
    },
    429: {
        "raise_exception": SendwithusRateLimitError,
        "message": "The API rate limit for your organisation/application pairing has been exceeded."
    },
    500: {
        "raise_exception": SendwithusInternalServerError,
        "message": "The server encountered an unexpected condition which prevented it from fulfilling the request."
    },
    501: {
        "raise_exception": SendwithusNotImplementedError,
        "message": "The server does not support the functionality required to fulfill the request."
    },
    502: {
        "raise_exception": SendwithusBadGatewayError,
        "message": "Server received an invalid response."
    },
    503: {
        "raise_exception": SendwithusServiceUnavailableError,
        "message": "API service is currently unavailable."
    }
}
