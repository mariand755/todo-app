import contextvars
import logging
import os

request_id_context: contextvars.ContextVar[str] = contextvars.ContextVar("request_id", default="-")


class RequestIdFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        record.request_id = request_id_context.get()
        return True


# This function retrieves the log level from the environment variable "LOG_LEVEL".
# It defaults to "INFO" if the variable is not set or if the provided value is invalid.
# The function uses the built-in logging module to convert the log level name to its corresponding integer
def _resolve_log_level() -> int:
    level_name = os.getenv("LOG_LEVEL", "INFO").upper()
    return getattr(logging, level_name, logging.INFO)


# This function configures the root logger with a specific format
# and adds a filter to include the request ID in log records.
# It also sets the log level based on an environment variable.
# If the root logger already has handlers, it updates their formatters
# and filters instead of adding new handlers.
def _configure_root_logger(level: int) -> None:
    root_logger = logging.getLogger()
    formatter = logging.Formatter("%(asctime)s %(levelname)s [%(name)s] [request_id=%(request_id)s] %(message)s")
    request_id_filter = RequestIdFilter()

    if not root_logger.handlers:
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        stream_handler.addFilter(request_id_filter)
        root_logger.addHandler(stream_handler)
    else:
        for handler in root_logger.handlers:
            handler.setFormatter(formatter)
            handler.addFilter(request_id_filter)

    root_logger.setLevel(level)


# This function is the main entry point for configuring logging in the application.
# It resolves the log level, configures the root logger,
# and sets the log level for uvicorn loggers to ensure that all logs from the application
# and the server are consistent with the specified log level
def configure_logging() -> None:
    level = _resolve_log_level()
    _configure_root_logger(level)
    logging.getLogger("uvicorn").setLevel(level)
    logging.getLogger("uvicorn.error").setLevel(level)
    logging.getLogger("uvicorn.access").setLevel(level)
