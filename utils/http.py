from fastapi.responses import JSONResponse


class APIResponse:
    @staticmethod
    def as_json(status_code: int, message: str, data: dict = None):
        content = {
            "code": status_code,
            "status": message,
        }
        if data is not None:
            content.update({"data": data})
        return JSONResponse(content=content, status_code=status_code)
