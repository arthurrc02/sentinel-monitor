import psutil


def collect_cpu_percent() -> float:
    """Uso de CPU (%) desde a última chamada. A primeira chamada do processo não é significativa."""
    return psutil.cpu_percent(interval=None)
