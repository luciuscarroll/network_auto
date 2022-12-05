from pydantic import BaseModel
from schemas.enums import Router_Enum
from typing import Optional, List

class DeviceInfo(BaseModel):
    name: Optional[str] = None
    ipAddress: Optional[str] = None

class DeviceInfoRemoteIds(BaseModel):
    ipAddress: str
    remote_ids: List[str]
    device_type: Router_Enum

class ClearBindingResponse(BaseModel):
    cleared: Optional[List[str]] = []
    not_bound: Optional[List[str]] = []

    class Config:
        orm_mode = True