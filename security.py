"""
Autenticação com JWT 

Contém:
  - hash e verificação de senha (usado por quem criar o endpoint de cadastro)
  - geração do token JWT (usado no login)
  - get_current_user: dependency que os colegas devem colocar em QUALQUER
    rota que precise exigir usuário logado (atualizar usuário, remover
    usuário, rotas de avaliação no TDE2, etc.)
"""
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from database import get_db
import models

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "chave-temporaria-trocar-no-env")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# tokenUrl aponta para a rota de login lá do main.py
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def hash_password(senha: str) -> str:
    return pwd_context.hash(senha)


def verify_password(senha_plana: str, senha_hash: str) -> bool:
    return pwd_context.verify(senha_plana, senha_hash)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expira_em = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expira_em})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> models.Usuario:
    """
    Dependency que valida o token JWT e retorna o usuário logado.

    Como usar em outra rota (exemplo para Allan/Lucas):

        @app.put("/usuarios/{usuario_id}")
        def atualizar_usuario(
            usuario_id: int,
            usuario_logado: models.Usuario = Depends(get_current_user),
            db: Session = Depends(get_db),
        ):
            ...
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido ou expirado",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    usuario = db.query(models.Usuario).filter(models.Usuario.email == email).first()
    if usuario is None:
        raise credentials_exception
    return usuario
