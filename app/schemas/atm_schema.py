from pydantic import BaseModel, Field, field_validator
from typing import Optional

class ATMCreate(BaseModel):
    bank_name: str = Field(..., min_length=2)
    address: Optional[str] = None
    latitude: float
    longitude: float
    is_active: bool = True

    # Validador para converter 'on' (do checkbox HTML) para Boolean
    @field_validator('is_active', mode='before')
    @classmethod
    def checkbox_to_bool(cls, v):
        if v in ('on', 'true', '1'): return True
        if v in ('off', 'false', '0', None): return False
        return v

class ATMResponse(BaseModel):
    id: int
    bank_name: str
    address: str
    latitude: float
    longitude: float
    is_active: bool

    class Config:
        from_attributes = True

class ATMUpdate(BaseModel):
    bank_name: str | None = None
    address: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    is_active: bool | None = None
    
    class Config:
        from_attributes = True

class ATMListResponse(BaseModel):
    atms: list[ATMResponse]

    class Config:
        from_attributes = True



