from typing import Optional, Union, Literal

from pydantic import BaseModel, Field

class IntMeasure(BaseModel):
    measure_type: Literal["int"]
    min_val: int = Field(...)
    max_val: int = Field(...)
    mean_val: Optional[int]
    std_val: Optional[int]

class FloatMeasure(BaseModel):
    measure_type: Literal["float"]
    min_val: float = Field(...)
    max_val: float = Field(...)
    mean_val: Optional[float]
    std_val: Optional[float]

class StrMeasure(BaseModel):
    measure_type: Literal["str"]
    min_val: str = Field(...)
    max_val: str = Field(...)
    mean_val: Optional[str]
    std_val: Optional[str]

class BoolMeasure(BaseModel):
    measure_type: Literal["bool"]
    min_val: bool = Field(...)
    max_val: bool = Field(...)
    mean_val: Optional[bool]
    std_val: Optional[bool]

class Measure(BaseModel):
    measure_id: str = Field(...)
    measure_name: str = Field(...)
    measure: Union[IntMeasure, FloatMeasure, StrMeasure, BoolMeasure] = Field(..., discriminator="measure_type")
    error_rate: float = Field(...)
