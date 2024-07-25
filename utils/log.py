import logging
import structlog
from structlog.stdlib import filter_by_level, add_logger_name, add_log_level


def configure_structlog():
    structlog.configure(
        processors=[
            filter_by_level,  # Filter logs based on severity
            add_logger_name,  # Add the logger name to the event
            add_log_level,  # Add the log level to the event
            structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S"),
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,  # Include exception details
            structlog.dev.ConsoleRenderer(),  # Pretty logs in development
        ],
        context_class=structlog.threadlocal.wrap_dict(dict),
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )


def disable_uvicorn_loggers():
    logging.getLogger("uvicorn.access").handlers = []
    logging.getLogger("uvicorn").handlers = []


logger: structlog.PrintLogger = structlog.get_logger(__name__)
