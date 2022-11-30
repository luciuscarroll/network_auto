from pydantic import BaseModel
from schemas.enums import Router_Enum
from typing import Optional

class DeviceInfo(BaseModel):
    name: str | None
    ipAddress: str | None

class DeviceInfoRemoteIds(BaseModel):
    ipAddress: str
    remote_ids: list[str]
    device_type: Router_Enum

class ClearBindingResponse(BaseModel):
    cleared: Optional[list[str]] = []
    not_bound: Optional[list[str]] = []

    class Config:
        orm_mode = True