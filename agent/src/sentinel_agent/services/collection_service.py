from datetime import UTC, datetime

from sentinel_agent.collectors.cpu import collect_cpu_percent
from sentinel_agent.collectors.disk import collect_disk_percent
from sentinel_agent.collectors.memory import collect_memory_percent
from sentinel_agent.models.metric_sample import MetricSample


def collect_metrics() -> MetricSample:
    """Coleta uma amostra de CPU, memória e disco no instante atual."""
    return MetricSample(
        cpu_percent=collect_cpu_percent(),
        memory_percent=collect_memory_percent(),
        disk_percent=collect_disk_percent(),
        collected_at=datetime.now(UTC),
    )
