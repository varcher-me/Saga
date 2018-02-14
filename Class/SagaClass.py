class SagaClass:
    params = None

    def set_param(self, key, value):
        self.params[key] = value

    def get_param(self, key):
        try:
            return self.params[key]
        except Exception as e:
            return None