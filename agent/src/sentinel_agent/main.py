"""Ponto de entrada do Sentinel Agent.

A coleta de métricas ainda não foi implementada — este módulo existe apenas
como esqueleto executável para a Sprint 0.
"""

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("sentinel_agent")


def main() -> None:
    logger.info("Sentinel Agent iniciado.")


if __name__ == "__main__":
    main()
