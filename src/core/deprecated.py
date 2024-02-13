import warnings
from functools import wraps

def deprecated(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        warnings.warn(f"Использование {func.__name__} устарело", DeprecationWarning)
        return func(*args, **kwargs)
    return decorator
