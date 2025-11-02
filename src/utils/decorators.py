from functools import wraps
from src.config import EXPECTED_NUM_ARGS


def input_error(func):
    """
    Decorator to handle input errors for command functions.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        command = func.__name__
        if command in EXPECTED_NUM_ARGS:
            num_args = EXPECTED_NUM_ARGS[command]
            if len(args) != num_args:
                return f"Error: {command}() takes {num_args} positional arguments but {len(args)} were given."
        return func(*args, **kwargs)

    return wrapper
