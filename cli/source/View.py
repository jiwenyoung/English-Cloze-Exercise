from functools import wraps

class View:
    @staticmethod
    def log(text):
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                print(text)
                return func(*args, **kwargs)
            return wrapper
        return decorator

    @staticmethod
    def render(text):
        print(text)
        return True

    @staticmethod
    def green(text):
        print(f"\033[1;32m{text}\033[0m")
        return True

    @staticmethod
    def red(text):
        print(f"\033[1;31m{text}\033[0m")
