from fastapi.testclient import TestClient

VALID_METRIC_PAYLOAD = {
    "cpu_percent": 42.5,
    "memory_percent": 60.0,
    "disk_percent": 75.3,
    "collected_at": "2026-07-22T10:00:00Z",
}


def _register_computer(client: TestClient, hostname: str = "pc-01") -> int:
    response = client.post("/computers", json={"hostname": hostname})
    id_: int = response.json()["id"]
    return id_


def test_record_metric_returns_201(client: TestClient) -> None:
    computer_id = _register_computer(client)

    response = client.post(f"/computers/{computer_id}/metrics", json=VALID_METRIC_PAYLOAD)

    assert response.status_code == 201
    body = response.json()
    assert body["computer_id"] == computer_id
    assert body["cpu_percent"] == VALID_METRIC_PAYLOAD["cpu_percent"]


def test_record_metric_for_unknown_computer_returns_404(client: TestClient) -> None:
    response = client.post("/computers/999/metrics", json=VALID_METRIC_PAYLOAD)

    assert response.status_code == 404


def test_list_metric_history_returns_recorded_metrics(client: TestClient) -> None:
    computer_id = _register_computer(client)
    client.post(f"/computers/{computer_id}/metrics", json=VALID_METRIC_PAYLOAD)

    response = client.get(f"/computers/{computer_id}/metrics")

    assert response.status_code == 200
    metrics = response.json()
    assert len(metrics) == 1
    assert metrics[0]["cpu_percent"] == VALID_METRIC_PAYLOAD["cpu_percent"]


def test_list_metric_history_for_unknown_computer_returns_404(client: TestClient) -> None:
    response = client.get("/computers/999/metrics")

    assert response.status_code == 404
