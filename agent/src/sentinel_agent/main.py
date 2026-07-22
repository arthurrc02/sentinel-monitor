"""Ponto de entrada do Sentinel Agent: registra a máquina e envia métricas periodicamente."""

import logging
import socket
import time

import httpx

from sentinel_agent.client.sentinel_client import SentinelApiClient
from sentinel_agent.collectors.cpu import collect_cpu_percent
from sentinel_agent.config import settings
from sentinel_agent.exceptions import SentinelApiError
from sentinel_agent.logging_config import configure_logging
from sentinel_agent.services.collection_service import collect_metrics
from sentinel_agent.services.registration_service import ensure_registered

logger = logging.getLogger("sentinel_agent")


def main() -> None:
    configure_logging(settings.log_level)
    hostname = settings.hostname or socket.gethostname()

    with SentinelApiClient(
        base_url=settings.api_base_url,
        timeout=settings.request_timeout_seconds,
        max_retry_attempts=settings.max_retry_attempts,
        retry_base_delay_seconds=settings.retry_base_delay_seconds,
    ) as client:
        computer_id = _register_with_retry(client, hostname)
        logger.info("agente registrado (computer_id=%s, hostname=%s)", computer_id, hostname)

        collect_cpu_percent()  # descarta a primeira leitura, sem janela de comparação

        try:
            while True:
                _collect_and_send(client, computer_id)
                time.sleep(settings.collection_interval_seconds)
        except KeyboardInterrupt:
            logger.info("encerrando o Sentinel Agent")


def _register_with_retry(client: SentinelApiClient, hostname: str) -> int:
    """Bloqueia até conseguir registrar (ou localizar) o computador na API."""
    while True:
        try:
            return ensure_registered(client, hostname)
        except (SentinelApiError, httpx.TransportError) as exc:
            logger.error("falha ao registrar computador, tentando novamente: %s", exc)
            time.sleep(settings.collection_interval_seconds)


def _collect_and_send(client: SentinelApiClient, computer_id: int) -> None:
    """Coleta e envia uma amostra; falhas aqui são logadas e não interrompem o loop."""
    try:
        sample = collect_metrics()
        client.send_metric(computer_id, sample)
        logger.info(
            "métrica enviada (cpu=%.1f%%, memory=%.1f%%, disk=%.1f%%)",
            sample.cpu_percent,
            sample.memory_percent,
            sample.disk_percent,
        )
    except SentinelApiError as exc:
        logger.error("falha ao enviar métrica: %s", exc)
    except httpx.TransportError as exc:
        logger.error("falha de conexão ao enviar métrica: %s", exc)


if __name__ == "__main__":
    main()
