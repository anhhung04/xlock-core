import os
from dotenv import load_dotenv

load_dotenv(override=True)

config = {
    "PORT": os.getenv("PORT", 8000),
    "HOST": "0.0.0.0",
    "workers": 4,
    "PROD": os.getenv("PROD", None),
    "ALLOWED_HOSTS": [
        "chrome-extension://oggondagbjepnifnnmcgdipgbemcimea",
        "http://localhost:3000",
        "http://185.111.159.172",
    ],
    "ALLOWED_METHODS": ["*"],
    "POSTGRES_SQL_URL": (
        f"postgresql://{os.getenv('POSTGRES_USER', 'postgres')}:"
        f"{os.getenv('POSTGRES_PASSWORD', 'postgres')}@"
        f"{os.getenv('POSTGRES_HOST', 'postgres')}:"
        f"{os.getenv('POSTGRES_PORT', '5432')}/"
        f"{os.getenv('POSTGRES_DB', 'postgres')}"
    ),
    "REDIS_HOST": os.getenv("REDIS_HOST", "redis"),
    "REDIS_PORT": os.getenv("REDIS_PORT", "6379"),
    "MAX_CONNECTIONS_REDIS": 20,
    "LOG_LEVEL": os.getenv("LOG_LEVEL", "INFO"),
    "SALT": os.getenv("PASSWORD_SALT", "xlock-salt"),
    "TOKEN_EXPIRE": os.getenv("TOKEN_EXPIRE", 86400),
}
