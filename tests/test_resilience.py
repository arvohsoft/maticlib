import pytest
from maticlib.resilience.retry import RetryPolicy, with_retry
from maticlib.exceptions import RetryExhaustedError


def test_retry_policy_success():
    counter = 0

    def flaky_func():
        nonlocal counter
        counter += 1
        if counter < 2:
            raise ValueError("Fail!")
        return "Success"

    policy = RetryPolicy(max_retries=3, initial_delay=0.01)
    result = policy.execute(flaky_func)
    assert result == "Success"
    assert counter == 2


def test_retry_policy_exhausted():
    def failing_func():
        raise ValueError("Always fails")

    policy = RetryPolicy(max_retries=2, initial_delay=0.01)
    with pytest.raises(RetryExhaustedError):
        policy.execute(failing_func)


def test_with_retry_decorator():
    counter = 0

    @with_retry(max_retries=3, initial_delay=0.01)
    def test_func():
        nonlocal counter
        counter += 1
        if counter < 3:
            raise ValueError("Fail")
        return "OK"

    assert test_func() == "OK"
    assert counter == 3
