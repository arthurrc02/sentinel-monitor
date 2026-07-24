import logging
import time
from collections.abc import Callable
from typing import TypeVar

logger = logging.getLogger(__name__)

T = TypeVar("T")


def with_retry(
    func: Callable[[], T],
    *,
    max_attempts: int,
    base_delay: float,
    should_retry: Callable[[Exception], bool],
    sleep: Callable[[float], None] = time.sleep,
) -> T:
    """Executa `func`, retentando com backoff exponencial (`base_delay * 2**tentativa`).

    Só retenta exceções para as quais `should_retry` retorna True; na última tentativa
    (ou para uma exceção não retentável) a exceção original é propagada.
    """
    for attempt in range(1, max_attempts + 1):
        try:
            return func()
        except Exception as exc:
            if attempt == max_attempts or not should_retry(exc):
                raise
            delay = base_delay * (2 ** (attempt - 1))
            logger.warning(
                "tentativa %s/%s falhou (%s), tentando novamente em %.1fs",
                attempt,
                max_attempts,
                exc,
                delay,
            )
            sleep(delay)

    raise AssertionError("with_retry requer max_attempts >= 1")
