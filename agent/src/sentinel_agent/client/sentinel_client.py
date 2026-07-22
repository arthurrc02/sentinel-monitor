from types import TracebackType
from typing import Any, Self

import httpx

from sentinel_agent.exceptions import SentinelApiError
from sentinel_agent.models.computer import Computer
from sentinel_agent.models.metric_sample import MetricSample
from sentinel_agent.utils.retry import with_retry


class SentinelApiClient:
    """Cliente HTTP para a API do Sentinel. Cada requisição é retentada com backoff exponencial."""

    def __init__(
        self,
        base_url: str,
        timeout: float,
        max_retry_attempts: int,
        retry_base_delay_seconds: float,
        transport: httpx.BaseTransport | None = None,
    ) -> None:
        self._client = httpx.Client(base_url=base_url, timeout=timeout, transport=transport)
        self._max_retry_attempts = max_retry_attempts
        self._retry_base_delay_seconds = retry_base_delay_seconds

    def register_computer(self, hostname: str) -> Computer:
        response = self._request("POST", "/computers", json={"hostname": hostname})
        return Computer.model_validate(response.json())

    def list_computers(self) -> list[Computer]:
        response = self._request("GET", "/computers")
        return [Computer.model_validate(item) for item in response.json()]

    def send_metric(self, computer_id: int, sample: MetricSample) -> None:
        self._request(
            "POST",
            f"/computers/{computer_id}/metrics",
            json=sample.model_dump(mode="json"),
        )

    def close(self) -> None:
        self._client.close()

    def __enter__(self) -> Self:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        self.close()

    def _request(self, method: str, url: str, **kwargs: Any) -> httpx.Response:
        def attempt() -> httpx.Response:
            response = self._client.request(method, url, **kwargs)
            if response.status_code >= 400:
                raise SentinelApiError(response.status_code, _extract_detail(response))
            return response

        return with_retry(
            attempt,
            max_attempts=self._max_retry_attempts,
            base_delay=self._retry_base_delay_seconds,
            should_retry=_is_retriable,
        )


def _is_retriable(exc: Exception) -> bool:
    if isinstance(exc, httpx.TransportError):
        return True
    return isinstance(exc, SentinelApiError) and exc.status_code >= 500


def _extract_detail(response: httpx.Response) -> str:
    try:
        body = response.json()
    except ValueError:
        return response.text
    if isinstance(body, dict) and "detail" in body:
        return str(body["detail"])
    return response.text
