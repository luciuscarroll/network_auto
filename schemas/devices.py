from pydantic import BaseModel
from schemas.enums import Router_Enum

class DeviceInfo(BaseModel):
    id: int | None
    name: str | None
    ipAddress: str | None

class DeviceInfoRemoteIds(BaseModel):
    ipAddress: str
    remote_ids: list[str]
    device_type: Router_Enum

class ClearBindingResponse(BaseModel):
    cleared: list[str] = []
    not_bound: list[str] = []

    class Config:
        orm_mode = True

class SevoneGroup(BaseModel):
    id: int | None
    name: str | None
