from pydantic import validate_email
from uuid import UUID


class ValidateInput:
    @staticmethod
    def is_email(email: str) -> bool:
        try:
            validate_email(email)
            return True
        except Exception:
            return False

    @staticmethod    
    def is_uuid(uuid: UUID) -> bool:
        try:
            UUID(str(uuid))
            return True
        except Exception:
            return False