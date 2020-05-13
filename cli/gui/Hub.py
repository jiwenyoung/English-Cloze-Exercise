import inspect

class NoMethodException(Exception):
    pass

class InvalidInvokeException(Exception):
    pass

class Hub:
    def __init__(self, Instance, user_token, correct_token):
        if user_token != correct_token:
            raise InvalidInvokeException
        else:
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