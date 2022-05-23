from typing import Optional

from pydantic import BaseModel, EmailStr, Field

class Device(BaseModel):
    device_id: str
    measure: str