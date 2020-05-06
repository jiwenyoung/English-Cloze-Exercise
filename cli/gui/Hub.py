import inspect

class NoMethodException(Exception):
    pass

class Hub:
    def __init__(self, Instance):
        self.instance = Instance()
        self.function = object()

    def is_yield_function(self,name):
        if hasattr(self.instance,name):
            function = getattr(self.instance,name)
            if inspect.isgeneratorfunction(function):
                return True
            else:
                return False

    def register(self, name):
        if hasattr(self.instance, name):
            function = getattr(self.instance, name)
            if callable(function):
                self.function = function
            else:
                raise NoMethodException(f"{name} is not callable")
            return self
        else:
            classname = type(self.instance).__name__
            raise NoMethodException(
                f"{name} method does not exist in {classname}"
            )

    def run(self, arguments):
        response = self.function(*arguments)
        return response

    def generate(self,arguments):
        for item in self.function(*arguments):
            yield item