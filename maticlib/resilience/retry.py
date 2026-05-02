import time
import logging
from typing import Callable, Type, Tuple, Any
from maticlib.exceptions import RetryExhaustedError

class RetryPolicy:
    def __init__(
        self,
        max_retries: int = 3,
        backoff_factor: float = 2.0,
        initial_delay: float = 1.0,
        exceptions: Tuple[Type[Exception], ...] = (Exception,),
        logger: logging.Logger = None,
    ):
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor
        self.initial_delay = initial_delay
        self.exceptions = exceptions
        self.logger = logger or logging.getLogger(__name__)

    def execute(self, func: Callable[..., Any], *args, **kwargs) -> Any:
        delay = self.initial_delay
        last_exception = None
        
        for attempt in range(1, self.max_retries + 1):
            try:
                return func(*args, **kwargs)
            except self.exceptions as e:
                last_exception = e
                if attempt == self.max_retries:
                    self.logger.error(f"Attempt {attempt}/{self.max_retries} failed for {func.__name__}. Exhausted.")
                    break
                
                self.logger.warning(f"Attempt {attempt}/{self.max_retries} failed for {func.__name__}. Retrying in {delay}s...")
                time.sleep(delay)
                delay *= self.backoff_factor
                
        raise RetryExhaustedError(f"Function {func.__name__} failed after {self.max_retries} attempts. Last error: {last_exception}") from last_exception

def with_retry(
    max_retries: int = 3,
    backoff_factor: float = 2.0,
    initial_delay: float = 1.0,
    exceptions: Tuple[Type[Exception], ...] = (Exception,)
):
    """Decorator to apply a retry policy to a function."""
    def decorator(func: Callable):
        policy = RetryPolicy(
            max_retries=max_retries,
            backoff_factor=backoff_factor,
            initial_delay=initial_delay,
            exceptions=exceptions
        )
        def wrapper(*args, **kwargs):
            return policy.execute(func, *args, **kwargs)
        return wrapper
    return decorator
