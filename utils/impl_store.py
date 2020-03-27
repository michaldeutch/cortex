class ImplementationStore:
    def __init__(self):
        self.implementations = {}

    def implementation(self, name):
        def add_implementation(cls):
            self.implementations[name] = cls
            return cls
        return add_implementation

    def get_impl(self, name):
        return self.implementations[name]
