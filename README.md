# TDE 1 - Back-end

API em FastAPI com autenticação JWT e CRUD de usuário.

## Equipe

- Açucena
- Allan Kennedy
- Felipe Oliveira
- Lucas Kevyn
- Murilo
- Stephanie

## Rotas

| Método | Rota | Descrição |
|---|---|---|
| POST | `/usuarios` | cria usuário |
| POST | `/login` | retorna o token JWT (no campo `username` vai o email) |
| GET | `/perfil` | dados do usuário logado |
| PATCH | `/usuarios/{id}` | atualiza usuário |
| DELETE | `/usuarios/{id}` | remove (desativa) usuário |
| DELETE | `/usuarios/{id}/permanente` | deleta usuário do banco |

Todas as rotas, menos cadastro e login, precisam do token.

### Regras

Atualização:
- usuário comum só edita ele mesmo, admin edita qualquer um
- pode alterar `nome`, `email` e `senha`
- `tipo` só admin altera, e não pode alterar o próprio
- pra trocar a própria senha tem que mandar `senha_atual`
- `id` e `ativo` não podem ser alterados
- se mudar o email precisa logar de novo

Remoção: usuário comum só remove ele mesmo, admin remove qualquer um menos ele mesmo.

Deleção: só admin, apaga também os registros em `usuario_curso` e `usuario_disciplina`.

## Banco de dados

SGBD: SQLite. O script `schema.sql` cria as tabelas e insere os dados de
exemplo. Ele roda automaticamente quando o servidor sobe e o banco ainda
não existe. Pra recriar o banco é só apagar o `tde.db`.

Usuários de exemplo:

| Email | Senha | Tipo |
|---|---|---|
| admin@exemplo.com | 123456 | admin |
| autor1@exemplo.com | 654321 | autor |
| autor2@exemplo.com | 213246 | autor |

## Como rodar

Precisa de Python 3.10+.

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env       # colocar uma SECRET_KEY (openssl rand -hex 32)
uvicorn main:app --reload
```

Documentação e testes das rotas em http://127.0.0.1:8000/docs
