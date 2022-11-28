from typing import Optional
from pydantic import BaseModel, ValidationError, validator


class TranscieverInput(BaseModel):
    tranciever: str

    @validator("tranciever")
    def value_check(cls, v):
        checker = v.split("/")
        if len(checker) != 3:
            raise ValueError("Must be in the form of tex/x/x")
        return v
