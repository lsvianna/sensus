# Sensus

Sensus e uma aplicacao Flask para analytics de contas publicas do Instagram. Esta versao roda com backend e frontend no mesmo servidor Flask, sem React e sem Node.js.

## Requisitos

- Python 3.12 recomendado
- Git
- VS Code no Windows ou GitHub Codespaces

Node.js nao e necessario.

## Rodar no Windows

No PowerShell, na raiz do projeto:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env -ErrorAction SilentlyContinue
python app.py
```

Se o ambiente Windows ja foi criado diretamente na raiz desta copia, ative-o com `.\Scripts\Activate.ps1` antes de instalar ou rodar o app.

Acesse:

```text
http://localhost:3000
```

Health check:

```text
http://localhost:3000/api/health
```

## Rodar no GitHub Codespaces

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
cp -n .env.example .env
python app.py
```

Abra a porta `3000` no Codespaces e acesse a URL encaminhada pelo GitHub.

## Banco de dados local

Por padrao o projeto usa SQLite:

```env
DATABASE_URL=sqlite:///instance/instagram_analytics.db
```

Isso funciona no Windows e no Codespaces sem PostgreSQL, Docker ou Redis. O banco e criado automaticamente quando o Flask inicia.

## Demo local

Na tela inicial, use `Carregar demo local` para criar dados de teste. O endpoint usado e:

```http
POST /api/demo/seed
```

Usuario criado:

```text
email: demo@sensus.local
senha: demo123
```

## Estrutura ativa

```text
app.py                         # Entrada do servidor Flask
config.py                      # Configuracao por ambiente
app/                           # Backend Flask
app/templates/index.html       # Frontend HTML
app/static/css/styles.css      # Estilos
app/static/js/main.js          # Interacao com a API
instance/                      # SQLite local
frontend/README.md             # Nota sobre a remocao do React
```

## API principal

```text
GET  /api/health
POST /api/auth/signup
POST /api/auth/login
GET  /api/accounts?user_id=1
POST /api/accounts
GET  /api/accounts/<id>/analytics
GET  /api/accounts/<id>/posts
POST /api/demo/seed
```

## Observacoes

- `gunicorn` continua no projeto para execucao Linux/Codespaces/Docker, mas no Windows use `python app.py`.
- Celery/Redis sao opcionais. Para habilitar jobs, instale `requirements-worker.txt` e configure `CELERY_BROKER_URL` e `CELERY_RESULT_BACKEND`. Sem broker, a analise roda de forma sincrona quando chamada.
- PostgreSQL e opcional: instale `requirements-postgres.txt` e use uma URL `postgresql+psycopg://...` em `DATABASE_URL`.
