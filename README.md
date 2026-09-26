# TDE - 1

Esta pasta contém a parte de **autenticação com JWT** do TDE1, pronta pra
rodar e pra ser integrada com o resto do projeto (criação/atualização/
remoção de usuário e, depois, gestão de avaliações).

## O que já está pronto
- Conexão com banco via SQLAlchemy (`database.py`)
- Modelo de usuário batendo com a tabela `usuario` do `schema.sql` da equipe (`models.py`)
- Hash de senha com bcrypt e geração/validação de token JWT (`security.py`)
- Rotas (`main.py`):
  - `POST /usuarios` — cadastro completo, com validações implementadas e tratamento de erros (placeholder para a Stephanie ajustar)
  - `POST /login` — autentica e devolve o token JWT (use o **e-mail** no campo "username", já que a tabela não tem coluna username)
  - `GET /perfil` — exemplo de rota **protegida** (só responde com token válido)
  

## Sobre o banco de dados
O arquivo `schema.sql` (enviado pela Stephanie) é carregado automaticamente
na primeira vez que o servidor sobe, criando todas as 10 tabelas do projeto
(usuario, curso, disciplina, questao, avaliacao etc.) e os 3 usuários de
exemplo — com as senhas já com hash bcrypt aplicado (as senhas originais em
texto puro eram: `admin@exemplo.com` = `123456`, `autor1@exemplo.com` =
`654321`, `autor2@exemplo.com` = `213246`).

Isso funciona automaticamente com **SQLite**. Se o time decidir usar
PostgreSQL ou MySQL, rodem o `schema.sql` direto no cliente do banco
escolhido (pgAdmin, MySQL Workbench etc.) e troquem a `DATABASE_URL` no
`.env` — nesse caso, pode apagar o trecho de auto-carregamento do
`schema.sql` em `main.py`, já que ele foi escrito para sintaxe do SQLite.

## Como rodar na sua máquina

1. **Ter o Python 3.10+ instalado.**

2. **Criar e ativar um ambiente virtual** (recomendado):
   ```bash
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   # Linux/Mac:
   source venv/bin/activate
   ```

3. **Instalar as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar o `.env`:**
   ```bash
   cp .env.example .env
   ```
   Depois abra o `.env` e gere uma `SECRET_KEY` de verdade com:
   ```bash
   openssl rand -hex 32
   ```
   (No Windows sem openssl, pode gerar em https://www.random.org/strings/ ou pedir pra IA gerar uma string aleatória de 64 caracteres.)

5. **Rodar o servidor:**
   ```bash
   uvicorn main:app --reload
   ```

6. **Abrir a documentação automática** no navegador:
   ```
   http://127.0.0.1:8000/docs
   ```
   Essa tela (Swagger) já deixa testar todas as rotas clicando, sem precisar de Postman.

## Como testar o fluxo manualmente

1. Em `/docs`, abra **POST /usuarios** → "Try it out" → preencha `nome`, `email`, `tipo` (ex: "autor"), `senha` → Execute.
2. Clique no botão **Authorize** (no topo da página) → no campo `username` digite o **e-mail** cadastrado, no `password` a senha → Authorize.
   - Também dá pra testar direto com um dos usuários de exemplo: `admin@exemplo.com` / `123456`.
3. Agora abra **GET /perfil** → "Try it out" → Execute. Deve retornar os dados do usuário logado.
4. Clique em **Authorize** de novo → **Logout** → tente `/perfil` outra vez → deve dar erro 401.

## Como integrar com o resto do time

- **Stephanie (script SQL):** o `models.py` já está batendo com a
  tabela `usuario` do `schema.sql` (colunas `id`, `email`, `nome`, `tipo`,
  `senha`). Se a tabela mudar, ajustem o `models.py` junto.
- **Felipe (criar usuário):** pode substituir a rota `POST /usuarios`
  deste `main.py` pela versão dela — só precisa continuar usando a função
  `hash_password()` de `security.py` para salvar a senha.
- **Allan (atualizar usuário) e Açucena (remover usuário):** no fim do
  `main.py` já tem um modelo comentado de como proteger a rota deles com
  `Depends(get_current_user)`. É só descomentar/adaptar e implementar a
  lógica de update/delete.
- **Banco de dados:** por padrão está usando SQLite (arquivo `tde.db`,
  criado automaticamente a partir do `schema.sql` na primeira execução).
  Quando decidirem o SGBD final, troquem a `DATABASE_URL` no `.env` e
  rodem o `schema.sql` direto no banco escolhido (instalem também o driver
  certo: `psycopg2-binary` para PostgreSQL ou `pymysql` para MySQL).

## Estrutura dos arquivos

```
tde_auth/
├── main.py           # rotas da API
├── security.py        # hash de senha + geração/validação de JWT
├── models.py           # modelo (tabela) do usuário
├── schemas.py          # formato dos dados de entrada/saída
├── database.py          # conexão com o banco
├── schema.sql            # script SQL da equipe (todas as tabelas + dados de exemplo)
├── requirements.txt      # dependências
└── .env.example          # exemplo de variáveis de ambiente
```

## Testado e funcionando
Este projeto foi testado de ponta a ponta (criação de usuário → login →
acesso a rota protegida → bloqueio sem token) e está funcionando.
