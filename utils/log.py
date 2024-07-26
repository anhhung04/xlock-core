import structlog
from config import config

processors = [
    structlog.stdlib.add_log_level,
    structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S"),
    structlog.processors.format_exc_info,
    structlog.processors.UnicodeDecoder(errors="backslashreplace"),
    structlog.processors.StackInfoRenderer(),
]

if config["PROD"]:
    processors.append(structlog.processors.JSONRenderer())
else:
    processors.extend(
        [
            structlog.dev.ConsoleRenderer(
                exception_formatter=structlog.dev.rich_traceback,
            ),
        ]
    )

structlog.configure(processors=processors)

logger: structlog.PrintLogger = structlog.getLogger("xlock")

__all__ = ["logger"]
