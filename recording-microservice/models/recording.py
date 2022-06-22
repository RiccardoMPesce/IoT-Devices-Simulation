from pydantic import BaseModel
from typing import Optional

class MeasureRecording(BaseModel):
    token: str
    username: Optional[str]

    class Config:
        orm_mode = True
