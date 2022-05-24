from typing import Optional
from numpy import double

from pydantic import BaseModel, Field

class DeviceSchema(BaseModel):
    device_id: str = Field(...)
    measure: str = Field(...)
    publish_qos: int = Field(..., ge=0, le=2)
    status: bool = Field(...)
    update_datetime: float = Field(..., ge=0.0)
    decading_factor: Optional[float] = Field()

    class Config:
        schema_extra = {
            "example": {
                "device_id": "D1927821-D37B-4C52-A5D3-0579CCFFC6B6",
                "measure": "temperature-room24",
                "publish-qos": 1,
                "status": "on",
                "update_datetime": 1653384081.510052
            }
        }

class UpdateDeviceModel(BaseModel):
    device_id: Optional[str]
    measure: Optional[str]
    publish_qos: Optional[int]
    status: bool = Optional[int]
    update_datetime: float

    class Config:
        schema_extra = {
            "example": {
                "device_id": "D1927821-D37B-4C52-A5D3-0579CCFFC6B6",
                "measure": "luminosity-room2",
                "publish-qos": 1,
                "status": "off",
                "update_datetime": 1653384081.540054
            }
        }