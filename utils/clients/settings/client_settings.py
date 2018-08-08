"""
Generic settings class for client access
"""


class ClientSettings(object):

    username = None
    password = None
    host = None
    port = None

    def __init__(self, username, password, host, port):
        self.username = self._attempt_param_cast(username)
        self.password = self._attempt_param_cast(password)
        self.host = self._attempt_param_cast(host)
        self.port = self._attempt_param_cast(port)

    @staticmethod
    def _attempt_param_cast(param):
        if not isinstance(param, str):
            raise ValueError("{0} of {1} is not a string".format(param, type(param)))
        return param
