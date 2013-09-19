"""
Exception classes
"""

class InvalidParameterError(StandardError):
    """
    Error when invalid parameter found in request
    """
    pass

class APIError(StandardError):
    """
    Error in response from api
    """
    def __init__(self, err_code, err_msg):
        super(APIError, self).__init__(self)
        self.err_code = err_code
        self.err_msg = err_msg

    def __repr__(self):
        return '%s: %s-%s' % (self.__class__.__name__,
                self.err_code, self.err_msg)

    def __str__(self):
        return '%s: %s-%s' % (self.__class__.__name__,
                self.err_code, self.err_msg)
