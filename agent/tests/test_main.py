from collections.abc import Callable

import httpx
import pytest

from sentinel_agent.client.sentinel_client import SentinelApiClient
from sentinel_agent.main import _collect_and_send, _register_with_retry


def test_register_with_retry_retries_until_success(
    build_client: Callable[..., SentinelApiClient], monkeypatch: pytest.MonkeyPatch
) -> None:
    """O loop externo de main.py deve seguir tentando registrar até a API responder bem."""
    monkeypatch.setattr("sentinel_agent.main.time.sleep", lambda _: None)

    attempts = {"count": 0}

    def handler(request: httpx.Request) -> httpx.Response:
        attempts["count"] += 1
        if attempts["count"] < 2:
            return httpx.Response(500, json={"detail": "erro interno"})
        return httpx.Response(
            201, json={"id": 1, "hostname": "pc-01", "created_at": "2026-07-22T10:00:00Z"}
        )

    # max_retry_attempts=1 no client: sem retry interno, para isolar o loop externo do main.py.
    client = build_client(handler, max_retry_attempts=1)

    computer_id = _register_with_retry(client, "pc-01")

    assert computer_id == 1
    assert attempts["count"] == 2


def test_collect_and_send_posts_metric(build_client: Callable[..., SentinelApiClient]) -> None:
    calls = {"count": 0}

    def handler(request: httpx.Request) -> httpx.Response:
        calls["count"] += 1
        return httpx.Response(
            201,
            json={
                "id": 1,
                "computer_id": 1,
                "cpu_percent": 1.0,
                "memory_percent": 1.0,
                "disk_percent": 1.0,
                "collected_at": "2026-07-22T10:00:00Z",
                "created_at": "2026-07-22T10:00:01Z",
            },
        )

    client = build_client(handler)

    _collect_and_send(client, 1)

    assert calls["count"] == 1


def test_collect_and_send_swallows_api_error(
    build_client: Callable[..., SentinelApiClient],
) -> None:
    """Uma falha ao enviar não deve propagar — o loop principal precisa seguir para o próximo
    ciclo.
    """

    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(500, json={"detail": "erro interno"})

    client = build_client(handler, max_retry_attempts=1)

    _collect_and_send(client, 1)  # não levanta


def test_collect_and_send_swallows_connection_error(
    build_client: Callable[..., SentinelApiClient],
) -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError("conexão recusada", request=request)

    client = build_client(handler, max_retry_attempts=1)

    _collect_and_send(client, 1)  # não levanta
