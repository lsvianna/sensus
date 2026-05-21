# 🎬 InstaBrush - Instagram Analytics Platform

Uma plataforma SaaS de análise de engajamento Instagram com **IA para sentimentos**, **Dashboard React em tempo real** e **API REST escalável**.

## 🎯 O que é?

**InstaBrush** monitora contas públicas do Instagram, analisa sentimentos dos comentários, identifica tendências e fornece insights acionáveis em tempo real.

### Perfil de Cliente
- 📊 Agências digitais
- 🎬 Criadores de conteúdo
- 🏢 Marcas que monitoram reputação
- 📈 Consultores de social media

### Como Funciona
1. Você conecta sua conta Instagram (pública)
2. Sistema coleta posts e comentários em tempo real
3. IA analisa sentimentos e tendências
4. Dashboard mostra métricas + insights
5. Exporte relatórios para clientes

---

## 📚 Tech Stack Aprendizado

### Backend (Python)
```
Flask              → Framework web (rotas, middleware)
SQLAlchemy         → ORM (banco de dados)
PostgreSQL         → DB production-ready
TextBlob/Transformers → IA/Sentimentos
JWT                → Autenticação segura
Celery + Redis     → Background jobs
```

**O que você vai aprender:**
- ✅ Arquitetura MVC profissional
- ✅ Modelagem de dados escalável
- ✅ APIs REST RESTful
- ✅ Integração com APIs externas
- ✅ Processamento de dados em batch
- ✅ Autenticação e autorização

### Frontend (React)
```
React 18           → UI components
Zustand            → State management
Styled Components  → CSS-in-JS
Axios              → HTTP client
Chart.js           → Dashboards
```

**O que você vai aprender:**
- ✅ Componentes reutilizáveis
- ✅ State management escalável
- ✅ Integração com APIs
- ✅ Dashboards em tempo real
- ✅ Performance optimization

### Infraestrutura
- Docker para containerização
- Gunicorn para produção
- PostgreSQL 15
- Redis para cache

---

## 🚀 Quick Start (5 min)

### 1️⃣ Backend

```bash
# Ativar venv
source .venv/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Copiar config
cp .env.example .env

# Criar banco de dados (localhost)
# Docker:
docker run --name postgres_ig -e POSTGRES_PASSWORD=postgres -p 5432:5432 -d postgres:15

# Ou usar SQLite pra MVP:
# (editar DATABASE_URL em config.py para sqlite:///:memory:)

# Rodar migrations
flask db upgrade

# Iniciar server
python app.py
# http://localhost:3000/api/health ✅
```

### 2️⃣ Frontend

```bash
cd frontend
npm install
npm start
# http://localhost:3000 🎉
```

---

## 📁 Estrutura de Pastas

```
app_teste/
├── app/                      # Backend Flask
│   ├── models/              # Banco de dados
│   │   └── models.py        # User, InstagramAccount, Post, Comment, Analysis
│   ├── routes/              # Endpoints da API
│   │   ├── auth.py         # Login/Signup
│   │   ├── accounts.py     # Manage contas
│   │   ├── posts.py        # Posts feed
│   │   └── analysis.py     # Analytics
│   ├── services/            # Lógica de negócio
│   │   ├── instagram_service.py    # API Instagram
│   │   └── sentiment_service.py    # IA sentimentos
│   └── utils/              # Helpers
├── frontend/               # React
│   ├── src/
│   │   ├── pages/         # Telas (Auth, Dashboard)
│   │   ├── components/    # Componentes (Analytics, Posts)
│   │   ├── api.js        # Cliente HTTP
│   │   └── store.js      # Estado global (Zustand)
│   └── package.json
├── app.py                 # Entrypoint
├── config.py             # Configurações
├── requirements.txt      # Deps Python
└── .env.example         # Variáveis de ambiente
```

---

## 🛠️ Endpoints API

### Auth
```bash
POST   /api/auth/signup    # Criar conta
POST   /api/auth/login     # Fazer login
```

### Contas
```bash
GET    /api/accounts              # Listar minhas contas
POST   /api/accounts              # Adicionar nova conta
GET    /api/accounts/:id          # Detalhes da conta
GET    /api/accounts/:id/analytics # Analytics da conta
```

### Posts
```bash
GET    /api/accounts/:id/posts    # Posts da conta
GET    /api/posts/:id             # Detalhes do post
GET    /api/posts/:id/analysis    # Análise sentimentos do post
```

### Health
```bash
GET    /api/health                # Status do server
```

---

## 🎯 Roadmap Aprendizado (3-4 semanas)

### Semana 1: Backend Fundação
- [x] Estrutura de pastas (MVC)
- [x] Modelos de dados (SQLAlchemy)
- [x] Endpoints básicos
- [ ] Autenticação JWT
- [ ] Banco de dados real (Postgres)

### Semana 2: Features Principais
- [ ] Integração Instagram API real
- [ ] Análise de sentimentos
- [ ] Background jobs (Celery)
- [ ] Testes unitários
- [ ] Documentação API (Swagger)

### Semana 3: Frontend & Real-time
- [ ] React components
- [ ] State management
- [ ] Gráficos interativos
- [ ] WebSocket (tempo real)
- [ ] Autenticação no frontend

### Semana 4: Produção
- [ ] CI/CD (GitHub Actions)
- [ ] Deploy (Heroku/AWS/DigitalOcean)
- [ ] Testes E2E
- [ ] Documentação de usuário
- [ ] Plano de pricing

---

## 🔗 Integração Instagram

### Opção 1: Instagram Graph API (Recomendado)
```
- Dados públicos apenas
- Requer approval Meta
- Gratuito para teste
- Limite: 200 requests/hora
```

### Opção 2: Web Scraping (Fallback)
```
- Dados públicos sem aprovação
- Mais rápido
- Risco: IP block
- Usar com cuidado
```

**Para MVP:** Mock data funciona 100%

---

## 💡 Ideias de Features

1. **Análise Temporal** → Entender quando melhor postar
2. **Detecção de Spam** → Filtrar comentários fake
3. **Recomendações** → "Poste sobre X para mais engajamento"
4. **Integração com Zapier** → Automações
5. **Reports em PDF** → Para vender aos clientes
6. **Comparação com Concorrentes** → Benchmarking
7. **Alertas** → Quando post vira viral ou bomba

---

## 🧪 Testando

```bash
# Backend health
curl http://localhost:3000/api/health

# Criar conta
curl -X POST http://localhost:3000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","password":"123","username":"testuser"}'

# Adicionar conta Instagram
curl -X POST http://localhost:3000/api/accounts \
  -H "Content-Type: application/json" \
  -d '{"user_id":1,"instagram_username":"instagram"}'

# Ver accounts
curl http://localhost:3000/api/accounts?user_id=1
```

---

## 📦 Deploy

### Heroku (mais fácil)
```bash
heroku create seu-app
heroku addons:create heroku-postgresql:hobby-dev
git push heroku main
```

### DigitalOcean (mais barato)
```bash
# Criar droplet Ubuntu
# SSH e rodar app.py com supervisord
```

### Docker
```bash
docker build -t instbrush .
docker run -p 3000:3000 instbrush
```

---

## 🤔 Próximos Passos

1. **Agora:** Rodar backend + frontend local ✅
2. **Next:** Conectar Postgres real
3. **After:** Integração Instagram API
4. **Then:** Deploy em produção
5. **Finally:** Vender! 💰

---

## 📖 Recursos de Aprendizado

- [Flask Documentation](https://flask.palletsprojects.com/)
- [React Documentation](https://react.dev/)
- [SQLAlchemy ORM](https://docs.sqlalchemy.org/)
- [Zustand State Management](https://github.com/pmndrs/zustand)
- [Instagram Graph API](https://developers.facebook.com/docs/instagram-graph-api/)

---

## 💬 Dúvidas?

Deixa eu saber! Podemos:
- Debugar erros
- Otimizar performance
- Adicionar features
- Refatorar código
- Preparar para deploy

**Vamos codar! 🚀**