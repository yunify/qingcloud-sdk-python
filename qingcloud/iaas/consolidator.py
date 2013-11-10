"""
Check parameters in request
"""
from qingcloud.iaas.errors import InvalidParameterError

class RequestChecker(object):

    error_msg = ''
    raise_error = True

    def __init__(self, raise_error=True):
        self.raise_error = raise_error

    def handle_error(self, error_msg):
        self.error_msg = error_msg
        if self.raise_error:
            raise InvalidParameterError(error_msg)
        else:
            print error_msg

    def check_integer(self, value):
        try:
            _ = int(value)
        except:
            return False
        return True

    def check_integer_params(self, directive, params):
        """ Specified params should be `int` type if in directive
            @param directive: the directive to check
            @param params: the params that should be `int` type.
        """
        for param in params:
            if param not in directive:
                continue
            val = directive[param]
            if self.check_integer(val):
                directive[param] = int(val)
            else:
                self.handle_error("parameter [%s] should be integer in directive [%s]" % (param, directive))
                return False
        return True

    def check_list_params(self, directive, params):
        """ Specified params should be `list` type if in directive
            @param directive: the directive to check
            @param params: the params that should be `list` type.
        """
        for param in params:
            if param not in directive:
                continue
            if not isinstance(directive[param], list):
                self.handle_error("parameter [%s] should be list in directive [%s]" % (param, directive))
                return False
        return True

    def check_required_params(self, directive, params):
        """ Specified params should be in directive
            @param directive: the directive to check
            @param params: the params that should be in directive.
        """
        for param in params:
            if param not in directive:
                self.handle_error("[%s] should be specified in directive [%s]" % (param, directive))
                return False
        return True

    def check_params(self, directive, required_params=None,
            integer_params=None, list_params=None):
        """ Check parameters in directive
            @param directive: the directive to check, should be `dict` type.
            @param required_params: a list of parameter that should be in directive.
            @param integer_params: a list of parameter that should be `integer` type
                                   if it exists in directive.
            @param list_params: a list of parameter that should be `list` type
                                if it exists in directive.
        """
        if not isinstance(directive, dict):
            self.handle_error('[%s] should be dict type' % directive)
            return False

        self.error_msg = ''
        if required_params:
            self.check_required_params(directive, required_params)
        if integer_params:
            self.check_integer_params(directive, integer_params)
        if list_params:
            self.check_list_params(directive, list_params)
        return self.error_msg == ''

    def check_sg_rules(self, rules):
        return all(self.check_params(rule,
            required_params=['priority', 'protocol'],
            integer_params=['priority', 'direction'],
            list_params=[]
            ) for rule in rules)

    def check_router_statics(self, statics):
        def check_router_static(static):
            # port forwarding
            if static.get('static_type') == 1:
                required_params = ['static_type', 'val1', 'val2', 'val3']
                integer_params = ['val1', 'val3']
            # vpn
            elif static.get('static_type') == 2:
                required_params = ['static_type']
                integer_params = ['val2']
            # dhcp
            elif static.get('static_type') == 3:
                required_params = ['static_type', 'val1', 'val2']
                integer_params = []
            else:
                required_params = []
                integer_params = []

            return self.check_params(static, required_params, integer_params)

        return all(check_router_static(static) for static in statics)
