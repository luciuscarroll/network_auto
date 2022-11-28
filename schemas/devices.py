from pydantic import BaseModel
from schemas.enums import Router_Enum

class DeviceInfo(BaseModel):
    name: str | None
    ipAddress: str | None

class DeviceInfoRemotIds(BaseModel):
    ipAddress: str
    remote_ids: list[str]
    device_type: Router_Enum

class ClearBindingResponse(BaseModel):
    cleared: list[str]
    not_bound: list[str]