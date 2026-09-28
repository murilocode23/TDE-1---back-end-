from typing import Optional
from pydantic import BaseModel, EmailStr


class UsuarioCreate(BaseModel):
    nome: str
    email: EmailStr
    tipo: str  # admin ou autor
    senha: str


class UsuarioUpdate(BaseModel):
    nome: Optional[str] = None
    email: Optional[EmailStr] = None
    tipo: Optional[str] = None
    senha: Optional[str] = None
    senha_atual: Optional[str] = None

    class Config:
        extra = "forbid"


class UsuarioOut(BaseModel):
    id: int
    nome: str
    email: EmailStr
    tipo: str

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str
