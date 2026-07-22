from sentinel_agent.collectors.cpu import collect_cpu_percent
from sentinel_agent.collectors.disk import collect_disk_percent
from sentinel_agent.collectors.memory import collect_memory_percent


def test_collect_cpu_percent_returns_value_in_range() -> None:
    assert 0.0 <= collect_cpu_percent() <= 100.0


def test_collect_memory_percent_returns_value_in_range() -> None:
    assert 0.0 <= collect_memory_percent() <= 100.0


def test_collect_disk_percent_returns_value_in_range() -> None:
    assert 0.0 <= collect_disk_percent() <= 100.0
