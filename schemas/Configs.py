from typing import Optional
from pydantic import BaseModel
from typing import Optional

class PhysicalInterface(BaseModel):
    transciever_type: str = Optional[None]
    transciever_part_number: str = Optional[None]
    laser_wavelength: str = Optional[None]
    transmit_power: str = Optional[None]
    recieve_power: str = Optional[None]
    vendor_name: str = Optional[None]
    interface: str = Optional[None]

