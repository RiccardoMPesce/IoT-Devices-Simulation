import time

from uuid import uuid4

from typing import Any, Optional, Union

from pydantic import BaseModel, Field

class Device(BaseModel):
    device_id: str = Field(uuid4())
    measure: str = Field(...)
    publish_qos: int = Field(..., ge=0, le=2)
    status: bool = Field(True)
    update_datetime: int = Field(int(time.time()), ge=0.0)

    class Config:
        schema_extra = {
            "example": {
                "device_id": "D1927821-D37B-4C52-A5D3-0579CCFFC6B6",
                "measure": "temperature-room24",
                "publish_qos": 1,
                "status": "on",
                "update_datetime": 1653384081
            }
        }

class UpdateDevice(BaseModel):
    device_id: Optional[str]
    measure: Optional[str]
    publish_qos: Optional[int]
    status: Optional[bool]
    update_datetime: int = Field(time.time(), ge=0.0)

    class Config:
        schema_extra = {
            "example": {
                "device_id": "D1927821-D37B-4C52-A5D3-0579CCFFC6B6",
                "measure": "luminosity-room2",
                "publish_qos": 1,
                "status": "off",
                "update_datetime": 1653384081
            }
        }
