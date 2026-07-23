from datetime import UTC, datetime

from fastapi.testclient import TestClient


def test_register_computer_returns_201(client: TestClient) -> None:
    response = client.post("/computers", json={"hostname": "pc-01"})

    assert response.status_code == 201
    body = response.json()
    assert body["hostname"] == "pc-01"
    assert "id" in body
    assert "created_at" in body


def test_register_duplicate_hostname_returns_409(client: TestClient) -> None:
    client.post("/computers", json={"hostname": "pc-01"})

    response = client.post("/computers", json={"hostname": "pc-01"})

    assert response.status_code == 409


def test_list_computers_returns_registered_computers(client: TestClient) -> None:
    client.post("/computers", json={"hostname": "pc-01"})
    client.post("/computers", json={"hostname": "pc-02"})

    response = client.get("/computers")

    assert response.status_code == 200
    hostnames = [computer["hostname"] for computer in response.json()]
    assert hostnames == ["pc-01", "pc-02"]


def test_computer_without_metrics_is_offline(client: TestClient) -> None:
    client.post("/computers", json={"hostname": "pc-01"})

    response = client.get("/computers")

    computer = response.json()[0]
    assert computer["is_online"] is False
    assert computer["last_seen_at"] is None


def test_computer_with_recent_metric_is_online(client: TestClient) -> None:
    computer_id = client.post("/computers", json={"hostname": "pc-01"}).json()["id"]
    recent = datetime.now(UTC).isoformat()
    client.post(
        f"/computers/{computer_id}/metrics",
        json={
            "cpu_percent": 1.0,
            "memory_percent": 1.0,
            "disk_percent": 1.0,
            "collected_at": recent,
        },
    )

    response = client.get("/computers")

    computer = response.json()[0]
    assert computer["is_online"] is True
    assert computer["last_seen_at"] is not None


def test_computer_with_stale_metric_is_offline(client: TestClient) -> None:
    computer_id = client.post("/computers", json={"hostname": "pc-01"}).json()["id"]
    client.post(
        f"/computers/{computer_id}/metrics",
        json={
            "cpu_percent": 1.0,
            "memory_percent": 1.0,
            "disk_percent": 1.0,
            "collected_at": "2020-01-01T00:00:00Z",
        },
    )

    response = client.get("/computers")

    computer = response.json()[0]
    assert computer["is_online"] is False
    assert computer["last_seen_at"] is not None
