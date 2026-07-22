from sentinel_agent.client.sentinel_client import SentinelApiClient
from sentinel_agent.exceptions import SentinelApiError


def ensure_registered(client: SentinelApiClient, hostname: str) -> int:
    """Garante que o computador esteja registrado e retorna seu `id`.

    Se o hostname já estiver registrado (409), busca o `id` na listagem em vez de falhar.
    """
    try:
        computer = client.register_computer(hostname)
        return computer.id
    except SentinelApiError as exc:
        if exc.status_code != 409:
            raise
        for computer in client.list_computers():
            if computer.hostname == hostname:
                return computer.id
        raise
