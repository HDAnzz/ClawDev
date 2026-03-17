import os
from functools import wraps


def require_api_key(key: str):
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            api_key = kwargs.get(key.lower())
            if not api_key:
                api_key = os.environ.get(key.upper())
            if not api_key:
                raise ValueError(
                    f"API key '{key}' not provided in kwargs or environment variable '{key.upper()}'"
                )
            return func(self, *args, **kwargs)

        return wrapper

    return decorator
