"""
Configuração da conexão com o banco de dados.

Por padrão usa SQLite (arquivo local "tde.db"), pra qualquer um do time
rodar o projeto sem precisar instalar um banco. Quando a equipe decidir
o SGBD definitivo (o Felipe cuida do script SQL), é só trocar a
DATABASE_URL abaixo — o resto do código não muda.

Exemplos de DATABASE_URL:
  SQLite (padrão):   sqlite:///./tde.db
  PostgreSQL:        postgresql://usuario:senha@localhost:5432/nome_do_banco
  MySQL:             mysql+pymysql://usuario:senha@localhost:3306/nome_do_banco
"""
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./tde.db")

# connect_args só é necessário para SQLite
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """Dependency do FastAPI: abre uma sessão do banco e garante que ela feche depois."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
