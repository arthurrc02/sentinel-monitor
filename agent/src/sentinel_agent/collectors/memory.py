import psutil


def collect_memory_percent() -> float:
    """Percentual de memória RAM em uso."""
    return psutil.virtual_memory().percent
