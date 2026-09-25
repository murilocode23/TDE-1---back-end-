"""
Aplicação principal do TDE1.

Este arquivo já traz pronto:
  - criação das tabelas no banco ao iniciar
  - POST /login          -> autentica e devolve o token JWT
  - GET  /perfil         -> exemplo de rota PROTEGIDA (exige token)
  - POST /usuarios       -> cadastro básico, só para o projeto rodar
                            de ponta a ponta. A Stephanie pode substituir
                            por uma versão mais completa.

Allan e Açucena: colem as rotas de atualizar/remover usuário aqui embaixo,
copiando o padrão da rota /perfil (usando Depends(get_current_user)).
"""
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

import os
from sqlalchemy import text

import models
import schemas
from database import engine, get_db
from security import hash_password, verify_password, create_access_token, get_current_user

# Cria o banco a partir do schema.sql da equipe (só roda se o banco ainda
# não tiver a tabela "usuario", pra não apagar dados toda vez que reiniciar).
with engine.connect() as conn:
    tabela_existe = conn.execute(
        text("SELECT name FROM sqlite_master WHERE type='table' AND name='usuario'")
    ).fetchone()
    if not tabela_existe:
        caminho_schema = os.path.join(os.path.dirname(__file__), "schema.sql")
        with open(caminho_schema, encoding="utf-8") as f:
            script_sql = f.read()
        for comando in script_sql.split(";"):
            comando = comando.strip()
            if comando:
                conn.execute(text(comando))
        conn.commit()

app = FastAPI(title="API - Gestão de Avaliações (TDE1)")


@app.post("/usuarios", response_model=schemas.UsuarioOut, status_code=201)
def criar_usuario(dados: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    """Cadastro básico de usuário (placeholder — Stephanie ajusta se precisar)."""
    ja_existe = db.query(models.Usuario).filter(models.Usuario.email == dados.email).first()
    if ja_existe:
        raise HTTPException(status_code=400, detail="E-mail já cadastrado")

    novo_usuario = models.Usuario(
        nome=dados.nome,
        email=dados.email,
        tipo=dados.tipo,
        senha=hash_password(dados.senha),
    )
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)
    return novo_usuario


@app.post("/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Login: no campo "username" do formulário, envie o E-MAIL do usuário
    (a tabela não tem coluna username). Devolve um token JWT se
    as credenciais estiverem corretas.
    """
    usuario = db.query(models.Usuario).filter(models.Usuario.email == form_data.username).first()
    if not usuario or not verify_password(form_data.password, usuario.senha):
        raise HTTPException(status_code=401, detail="E-mail ou senha incorretos")

    token = create_access_token({"sub": usuario.email})
    return {"access_token": token, "token_type": "bearer"}


@app.get("/perfil", response_model=schemas.UsuarioOut)
def perfil(usuario_logado: models.Usuario = Depends(get_current_user)):
    """Rota protegida de exemplo — só responde se o token for válido."""
    return usuario_logado


# --------------------------------------------------------------------------
# Allan (atualizar usuário) e Açucena (remover usuário): usem este modelo
# --------------------------------------------------------------------------
#
# @app.put("/usuarios/{usuario_id}", response_model=schemas.UsuarioOut)
# def atualizar_usuario(
#     usuario_id: int,
#     dados: schemas.UsuarioCreate,
#     usuario_logado: models.Usuario = Depends(get_current_user),
#     db: Session = Depends(get_db),
# ):
#     ...
#
# @app.delete("/usuarios/{usuario_id}", status_code=204)
# def remover_usuario(
#     usuario_id: int,
#     usuario_logado: models.Usuario = Depends(get_current_user),
#     db: Session = Depends(get_db),
# ):
#     ...
