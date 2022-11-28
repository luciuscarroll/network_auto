from pydantic import BaseModel, ValidationError, validator
from schemas.enums import Router_Enum
from schemas.devices import DeviceInfoRemotIds

class TranscieverInput(BaseModel):
    tranciever: str
    router_ip: str
    device_type: Router_Enum

    @validator("tranciever")
    def value_check(cls, v):
        checker = v.split("/")
        if len(checker) != 3:
            raise ValueError("Must be in the form of tex/x/x")
        return v


class ClearBindingsInput(BaseModel):
    devices: list[DeviceInfoRemotIds]