from typing import Annotated
from fastapi import Header, Path

AUTH_HEADER = "Authorization"

TokenHeader = Annotated[str, Header(alias=AUTH_HEADER)]

IdPath = Annotated[
    str, Path(regex=r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$")
]
