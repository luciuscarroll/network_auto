from pydantic import BaseModel, ValidationError, validator
from schemas.enums import Router_Enum

class TranscieverInput(BaseModel):
    tranciever: str
    host: str
    device_type: Router_Enum

    @validator("tranciever")
    def value_check(cls, v):
        checker = v.split("/")
        if len(checker) > 4 or len(checker) < 3:
            raise ValueError("Cisco XE transciever must be in the form of tex/x/x/x")
        return v

class Message(BaseModel):
    message: str


# class Response(BaseModel):
# status_code: str
# details: any

