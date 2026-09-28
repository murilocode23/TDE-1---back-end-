from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import os
from sqlalchemy import text

import models
import schemas
from database import engine, get_db
from security import hash_password, verify_password, create_access_token, get_current_user

# cria o banco pelo schema.sql se ainda nao existir
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

TIPOS_VALIDOS = {"admin", "autor"}
@app.post("/usuarios", response_model=schemas.UsuarioOut, status_code=201)
def criar_usuario(dados: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    nome = dados.nome.strip()
    email = dados.email.lower()
    senha = dados.senha
    tipo = dados.tipo

    if not nome:
        raise HTTPException(status_code=422, detail="Nome é obrigatório")
    if len(nome) > 100:
        raise HTTPException(status_code=422, detail="Nome deve ter no máximo 100 caracteres")

    if len(senha) < 8:
        raise HTTPException(status_code=422, detail="Senha deve ter no mínimo 8 caracteres")

    if tipo not in TIPOS_VALIDOS:
        raise HTTPException(
            status_code=422,
            detail=f"Tipo deve ser um dos seguintes: {', '.join(sorted(TIPOS_VALIDOS))}",
        )

    ja_existe = db.query(models.Usuario).filter(models.Usuario.email == email).first()
    if ja_existe:
        raise HTTPException(status_code=400, detail="E-mail já cadastrado")

    novo_usuario = models.Usuario(
        nome=nome,
        email=email,
        tipo=tipo,
        senha=hash_password(senha),
    )
    db.add(novo_usuario)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="E-mail já cadastrado")
    db.refresh(novo_usuario)
    return novo_usuario


@app.post("/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # o campo username recebe o email
    usuario = db.query(models.Usuario).filter(models.Usuario.email == form_data.username, models.Usuario.ativo == True).first()
    if not usuario or not verify_password(form_data.password, usuario.senha):
        raise HTTPException(status_code=401, detail="E-mail ou senha incorretos")

    token = create_access_token({"sub": usuario.email})
    return {"access_token": token, "token_type": "bearer"}


@app.get("/perfil", response_model=schemas.UsuarioOut)
def perfil(usuario_logado: models.Usuario = Depends(get_current_user)):
    return usuario_logado

@app.delete("/usuarios/{usuario_id}", status_code=204)
def remover_usuario(
    usuario_id: int,
    usuario_logado: models.Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    eh_admin = usuario_logado.tipo == "admin"
    eh_proprio = usuario_logado.id == usuario_id

    if not eh_admin and not eh_proprio:
        raise HTTPException(status_code=403, detail="Você só pode remover o seu próprio usuário")
    if eh_admin and eh_proprio:
        raise HTTPException(status_code=403, detail="Administrador não pode remover o próprio usuário")

    usuario = db.query(models.Usuario).filter(
        models.Usuario.id == usuario_id, models.Usuario.ativo == True
    ).first()

    if not usuario:
        raise HTTPException(
            status_code=404,
            detail="Usuário não encontrado"
        )

    usuario.ativo = False

    db.commit()

    return


@app.delete("/usuarios/{usuario_id}/permanente", status_code=204)
def deletar_usuario(
    usuario_id: int,
    usuario_logado: models.Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if usuario_logado.tipo != "admin":
        raise HTTPException(status_code=403, detail="Apenas administradores podem deletar usuários")
    if usuario_logado.id == usuario_id:
        raise HTTPException(status_code=403, detail="Administrador não pode deletar o próprio usuário")

    usuario = db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    db.execute(text("DELETE FROM usuario_curso WHERE usuario_id = :id"), {"id": usuario_id})
    db.execute(text("DELETE FROM usuario_disciplina WHERE usuario_id = :id"), {"id": usuario_id})
    db.delete(usuario)
    db.commit()

    return


@app.patch("/usuarios/{usuario_id}", response_model=schemas.UsuarioOut)
def atualizar_usuario(
    usuario_id: int,
    dados: schemas.UsuarioUpdate,
    usuario_logado: models.Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    eh_admin = usuario_logado.tipo == "admin"
    eh_proprio = usuario_logado.id == usuario_id

    if not eh_admin and not eh_proprio:
        raise HTTPException(status_code=403, detail="Você só pode editar o seu próprio usuário")

    usuario = db.query(models.Usuario).filter(
        models.Usuario.id == usuario_id, models.Usuario.ativo == True
    ).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    alteracoes = dados.model_dump(exclude_unset=True)
    senha_atual = alteracoes.pop("senha_atual", None)

    if not alteracoes:
        raise HTTPException(status_code=400, detail="Nenhum campo para atualizar foi enviado")

    for campo, valor in alteracoes.items():
        if valor is None:
            raise HTTPException(status_code=422, detail=f"O campo '{campo}' não pode ser nulo")

    if "nome" in alteracoes:
        nome = alteracoes["nome"].strip()
        if not nome:
            raise HTTPException(status_code=422, detail="Nome é obrigatório")
        if len(nome) > 100:
            raise HTTPException(status_code=422, detail="Nome deve ter no máximo 100 caracteres")
        usuario.nome = nome

    if "email" in alteracoes:
        email = alteracoes["email"].lower()
        if email != usuario.email:
            ja_existe = db.query(models.Usuario).filter(
                models.Usuario.email == email, models.Usuario.id != usuario.id
            ).first()
            if ja_existe:
                raise HTTPException(status_code=400, detail="E-mail já cadastrado")
            usuario.email = email

    if "tipo" in alteracoes:
        tipo = alteracoes["tipo"]
        if not eh_admin:
            raise HTTPException(status_code=403, detail="Apenas administradores podem alterar o tipo do usuário")
        if eh_proprio and tipo != usuario.tipo:
            raise HTTPException(status_code=403, detail="Administrador não pode alterar o próprio tipo")
        if tipo not in TIPOS_VALIDOS:
            raise HTTPException(
                status_code=422,
                detail=f"Tipo deve ser um dos seguintes: {', '.join(sorted(TIPOS_VALIDOS))}",
            )
        usuario.tipo = tipo

    if "senha" in alteracoes:
        senha = alteracoes["senha"]
        if len(senha) < 8:
            raise HTTPException(status_code=422, detail="Senha deve ter no mínimo 8 caracteres")
        if eh_proprio:
            if not senha_atual or not verify_password(senha_atual, usuario.senha):
                raise HTTPException(status_code=400, detail="Senha atual incorreta ou não informada")
        usuario.senha = hash_password(senha)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="E-mail já cadastrado")
    db.refresh(usuario)
    return usuario


