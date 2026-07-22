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
