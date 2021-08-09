from pydantic import BaseModel

class BaseResponse(BaseModel):
    result: bool