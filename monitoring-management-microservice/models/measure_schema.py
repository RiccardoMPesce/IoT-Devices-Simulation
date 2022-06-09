from typing import Optional, Union, Literal

from pydantic import BaseModel, Field

class Measure(BaseModel):
    measure_id: str = Field(...)
    measure_name: str = Field(...)
    measure_value: Union[int, bool, float, str] = Field(...)
