"""
Retry Handler
Provides retry logic with exponential backoff for transient errors.
"""

import time
import logging
from functools import wraps
from typing import Callable, Type

class TransientError(Exception):
    """Base class for transient errors that should be retried"""
    pass

class NetworkError(TransientError):
    """Network-related errors"""
    pass

class RateLimitError(TransientError):
    """API rate limit errors"""
    pass

def with_retry(
    max_attempts: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    exceptions: tuple = (TransientError,)
):
    """
    Decorator to retry a function with exponential backoff.

    Args:
        max_attempts: Maximum number of retry attempts
        base_delay: Initial delay in seconds
        max_delay: Maximum delay in seconds
        exceptions: Tuple of exception types to catch and retry
    """
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            logger = logging.getLogger(func.__module__)

            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    if attempt == max_attempts - 1:
                        logger.error(f'{func.__name__} failed after {max_attempts} attempts')
                        raise

                    delay = min(base_delay * (2 ** attempt), max_delay)
                    logger.warning(
                        f'{func.__name__} attempt {attempt + 1} failed: {e}. '
                        f'Retrying in {delay}s...'
                    )
                    time.sleep(delay)
                except Exception as e:
                    # Non-transient error, don't retry
                    logger.error(f'{func.__name__} failed with non-transient error: {e}')
                    raise

        return wrapper
    return decorator

# Example usage
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    @with_retry(max_attempts=3, base_delay=1)
    def flaky_api_call():
        """Simulates a flaky API call"""
        import random
        if random.random() < 0.7:
            raise NetworkError("Connection timeout")
        return "Success!"

    try:
        result = flaky_api_call()
        print(result)
    except Exception as e:
        print(f"Failed: {e}")
