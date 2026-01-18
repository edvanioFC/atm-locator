from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional, Annotated

# Definimos um tipo reutilizável para a senha com no mínimo 8 caracteres
PasswordStr = Annotated[str, Field(min_length=8)]

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: PasswordStr
    
    @field_validator('password')
    @classmethod
    def validate_password(cls, v: str) -> str:
        if not any(char.isdigit() for char in v):
            raise ValueError('A senha deve conter pelo menos um número')
        if not any(char.isalpha() for char in v):
            raise ValueError('A senha deve conter pelo menos uma letra')
        return v

class UserLogin(BaseModel):
    username: str
    password: str

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[PasswordStr] = None
    
    @field_validator('password')
    @classmethod
    def validate_password(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            if not any(char.isdigit() for char in v):
                raise ValueError('A senha deve conter pelo menos um número')
            if not any(char.isalpha() for char in v):
                raise ValueError('A senha deve conter pelo menos uma letra')
        return v
    
class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        from_attributes = True