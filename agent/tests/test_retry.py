import pytest

from sentinel_agent.utils.retry import with_retry


class FlakyError(Exception):
    pass


class FatalError(Exception):
    pass


def test_returns_value_on_first_success() -> None:
    result = with_retry(
        lambda: 42,
        max_attempts=3,
        base_delay=1.0,
        should_retry=lambda exc: True,
        sleep=lambda _: None,
    )

    assert result == 42


def test_retries_until_success() -> None:
    attempts = {"count": 0}

    def flaky() -> str:
        attempts["count"] += 1
        if attempts["count"] < 3:
            raise FlakyError("temporário")
        return "ok"

    sleeps: list[float] = []
    result = with_retry(
        flaky,
        max_attempts=5,
        base_delay=1.0,
        should_retry=lambda exc: isinstance(exc, FlakyError),
        sleep=sleeps.append,
    )

    assert result == "ok"
    assert attempts["count"] == 3
    assert sleeps == [1.0, 2.0]


def test_raises_after_exhausting_attempts() -> None:
    def always_fails() -> None:
        raise FlakyError("sempre falha")

    with pytest.raises(FlakyError):
        with_retry(
            always_fails,
            max_attempts=3,
            base_delay=0.01,
            should_retry=lambda exc: True,
            sleep=lambda _: None,
        )


def test_does_not_retry_non_retriable_exception() -> None:
    calls = {"count": 0}

    def fails_once() -> None:
        calls["count"] += 1
        raise FatalError("não retentável")

    with pytest.raises(FatalError):
        with_retry(
            fails_once,
            max_attempts=5,
            base_delay=0.01,
            should_retry=lambda exc: isinstance(exc, FlakyError),
            sleep=lambda _: None,
        )

    assert calls["count"] == 1
