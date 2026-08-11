import logging
import sys


LOG_FORMAT = "%(asctime)s %(levelname)s [%(name)s] %(message)s"


def configure_logging() -> None:
    """Configure simple structured application logging."""

    logging.basicConfig(
        level=logging.INFO,
        format=LOG_FORMAT,
        stream=sys.stdout,
        force=True,
    )
