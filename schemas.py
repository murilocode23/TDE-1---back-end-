"""
Schemas Pydantic: definem o formato dos dados que entram e saem da API.
Os colegas que forem criar/atualizar usuário podem reaproveitar
UsuarioCreate e UsuarioOut aqui.
"""
from pydantic import BaseModel, EmailStr


class UsuarioCreate(BaseModel):
    nome: str
    email: EmailStr
    tipo: str  # ex: "admin" ou "autor"
    senha: str


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
