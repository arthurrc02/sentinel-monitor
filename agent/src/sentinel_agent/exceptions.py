class SentinelApiError(Exception):
    """Levantada quando a API do Sentinel responde com um status de erro."""

    def __init__(self, status_code: int, detail: str) -> None:
        self.status_code = status_code
        self.detail = detail
        super().__init__(f"API respondeu {status_code}: {detail}")
