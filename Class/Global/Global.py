class Global:
    __params = None

    def set_param(self, param_name, param_value):
        self.__params[param_name] = param_value
        return

    def get_param(self, param_name):
        return self.__params[param_name]



