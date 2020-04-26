from functools import wraps
import os

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
    def progress(total, index, width=60, char="=", end=">"):
        console_width = os.get_terminal_size().columns
        if console_width >= 60:
            width = 60
        else:
            width = console_width - 20
        progress = int(100 / total * (index + 1))
        now = int(width * (progress/100))
        print(f"Progress : {char * now}{end} {progress}%", end="\r")
        return View
