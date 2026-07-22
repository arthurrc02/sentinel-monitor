from collections.abc import Callable

import httpx
import pytest

from sentinel_agent.client.sentinel_client import SentinelApiClient
from sentinel_agent.exceptions import SentinelApiError
from sentinel_agent.services.registration_service import ensure_registered


def test_ensure_registered_returns_id_on_first_registration(
    build_client: Callable[..., SentinelApiClient],
) -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            201, json={"id": 7, "hostname": "pc-01", "created_at": "2026-07-22T10:00:00Z"}
        )

    computer_id = ensure_registered(build_client(handler), "pc-01")

    assert computer_id == 7


def test_ensure_registered_falls_back_to_list_on_conflict(
    build_client: Callable[..., SentinelApiClient],
) -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.method == "POST":
            return httpx.Response(409, json={"detail": "já existe"})
        return httpx.Response(
            200,
            json=[
                {"id": 3, "hostname": "outro-pc", "created_at": "2026-07-22T09:00:00Z"},
                {"id": 7, "hostname": "pc-01", "created_at": "2026-07-22T10:00:00Z"},
            ],
        )

    computer_id = ensure_registered(build_client(handler), "pc-01")

    assert computer_id == 7


def test_ensure_registered_raises_if_hostname_missing_from_list(
    build_client: Callable[..., SentinelApiClient],
) -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.method == "POST":
            return httpx.Response(409, json={"detail": "já existe"})
        return httpx.Response(200, json=[])

    with pytest.raises(SentinelApiError):
        ensure_registered(build_client(handler), "pc-01")


def test_ensure_registered_propagates_non_conflict_errors(
    build_client: Callable[..., SentinelApiClient],
) -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(500, json={"detail": "erro interno"})

    with pytest.raises(SentinelApiError) as exc_info:
        ensure_registered(build_client(handler), "pc-01")

    assert exc_info.value.status_code == 500
