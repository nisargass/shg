import logging
import sys


def setup_logging(debug: bool = True) -> None:
    """Configures structured, privacy-safe logging for the AI microservice."""
    log_level = logging.DEBUG if debug else logging.INFO

    # Custom log format that excludes sensitive payload dumps
    log_format = "%(asctime)s [%(levelname)s] [%(name)s]: %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"

    logging.basicConfig(
        level=log_level,
        format=log_format,
        datefmt=date_format,
        handlers=[logging.StreamHandler(sys.stdout)],
        force=True
    )

    # Suppress verbose HTTP wire logs to protect credentials and payloads
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.access").setLevel(logging.INFO)


logger = logging.getLogger("ai_service")

