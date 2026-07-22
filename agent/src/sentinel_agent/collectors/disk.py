import psutil


def collect_disk_percent(path: str = "/") -> float:
    """Percentual de uso do disco que contém `path`."""
    return psutil.disk_usage(path).percent
