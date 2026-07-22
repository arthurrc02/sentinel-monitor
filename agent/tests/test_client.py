from collections.abc import Callable
from datetime import UTC, datetime

import httpx
import pytest

from sentinel_agent.client.sentinel_client import SentinelApiClient
from sentinel_agent.exceptions import SentinelApiError
from sentinel_agent.models.metric_sample import MetricSample


def _sample() -> MetricSample:
    return MetricSample(
        cpu_percent=1.0, memory_percent=2.0, disk_percent=3.0, collected_at=datetime.now(UTC)
    )


def test_register_computer_success(build_client: Callable[..., SentinelApiClient]) -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/computers"
        assert request.method == "POST"
        return httpx.Response(
            201, json={"id": 1, "hostname": "pc-01", "created_at": "2026-07-22T10:00:00Z"}
        )

    computer = build_client(handler).register_computer("pc-01")

    assert computer.id == 1
    assert computer.hostname == "pc-01"


def test_register_computer_conflict_raises_with_status_code(
    build_client: Callable[..., SentinelApiClient],
) -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(409, json={"detail": "já existe"})

    with pytest.raises(SentinelApiError) as exc_info:
        build_client(handler).register_computer("pc-01")

    assert exc_info.value.status_code == 409
    assert exc_info.value.detail == "já existe"


def test_list_computers_parses_response(build_client: Callable[..., SentinelApiClient]) -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200, json=[{"id": 1, "hostname": "pc-01", "created_at": "2026-07-22T10:00:00Z"}]
        )

    computers = build_client(handler).list_computers()

    assert len(computers) == 1
    assert computers[0].hostname == "pc-01"


def test_send_metric_posts_to_computer_metrics_path(
    build_client: Callable[..., SentinelApiClient],
) -> None:
    received_path = {}

    def handler(request: httpx.Request) -> httpx.Response:
        received_path["value"] = request.url.path
        return httpx.Response(
            201,
            json={
                "id": 1,
                "computer_id": 1,
                "cpu_percent": 1.0,
                "memory_percent": 2.0,
                "disk_percent": 3.0,
                "collected_at": "2026-07-22T10:00:00Z",
                "created_at": "2026-07-22T10:00:01Z",
            },
        )

    build_client(handler).send_metric(1, _sample())

    assert received_path["value"] == "/computers/1/metrics"


def test_retries_on_server_error_then_succeeds(
    build_client: Callable[..., SentinelApiClient],
) -> None:
    calls = {"count": 0}

    def handler(request: httpx.Request) -> httpx.Response:
        calls["count"] += 1
        if calls["count"] < 3:
            return httpx.Response(500, json={"detail": "erro interno"})
        return httpx.Response(200, json=[])

    build_client(handler, max_retry_attempts=5).list_computers()

    assert calls["count"] == 3


def test_does_not_retry_on_not_found(build_client: Callable[..., SentinelApiClient]) -> None:
    calls = {"count": 0}

    def handler(request: httpx.Request) -> httpx.Response:
        calls["count"] += 1
        return httpx.Response(404, json={"detail": "não encontrado"})

    with pytest.raises(SentinelApiError) as exc_info:
        build_client(handler, max_retry_attempts=5).send_metric(999, _sample())

    assert exc_info.value.status_code == 404
    assert calls["count"] == 1
