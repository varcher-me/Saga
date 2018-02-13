class TestHandler:
    __test = None

    def process(self, file_obj):
        print(file_obj.get_path_name())
