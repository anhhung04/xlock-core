import os
from dotenv import load_dotenv

load_dotenv(override=True)

config = {
    "PORT": 8000,
    "HOST": "0.0.0.0",
    "workers": 4,
    "PROD": os.getenv("PROD", None),
    "ALLOWED_HOSTS": ["*"],
    "POSTGRES_SQL_URL": (
        f"postgresql://{os.getenv('POSTGRES_USER', 'dev_user')}:"
        f"{os.getenv('POSTGRES_PASSWORD', 'secret')}@"
        f"{os.getenv('POSTGRES_HOST', 'database')}:"
        f"{os.getenv('POSTGRES_PORT', '5432')}/"
        f"{os.getenv('POSTGRES_DB', 'dev_xlock')}"
    ),
    "REDIS_HOST": os.getenv("REDIS_HOST", "redis"),
    "REDIS_PORT": os.getenv("REDIS_PORT", "6379"),
    "MAX_CONNECTIONS_REDIS": 20,
}
