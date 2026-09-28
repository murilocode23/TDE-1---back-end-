from sqlalchemy import Column, Integer, String, Boolean
from database import Base


class Usuario(Base):
    __tablename__ = "usuario"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    nome = Column(String(100), nullable=False)
    tipo = Column(String(20), nullable=False)
    senha = Column(String(255), nullable=False)  # hash bcrypt
    ativo = Column(Boolean, default=True, nullable=False)
