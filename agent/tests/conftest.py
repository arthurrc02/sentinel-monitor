from collections.abc import Callable

import httpx
import pytest

from sentinel_agent.client.sentinel_client import SentinelApiClient


@pytest.fixture
def build_client() -> Callable[..., SentinelApiClient]:
    """Factory fixture: cria um SentinelApiClient com transporte mockado (sem rede real)."""

    def _build(
        handler: Callable[[httpx.Request], httpx.Response],
        max_retry_attempts: int = 1,
        retry_base_delay_seconds: float = 0.001,
    ) -> SentinelApiClient:
        return SentinelApiClient(
            base_url="http://backend.test",
            timeout=5.0,
            max_retry_attempts=max_retry_attempts,
            retry_base_delay_seconds=retry_base_delay_seconds,
            transport=httpx.MockTransport(handler),
        )

    return _build
