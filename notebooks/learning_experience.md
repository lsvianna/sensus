## Experiência de Aprendizado — Análise de Sentimento e ML

Objetivo: usar o backend para analisar posts do Instagram (mock) e aprender sobre pipeline de NLP e experimentos ML.

Como usar:

1. Inicie a app Flask:

```bash
source .venv/bin/activate
export FLASK_APP=app:create_app
flask run --port=3000
```

2. Crie um usuário (signup) e faça login para obter `access_token`.

3. Adicione uma conta e poste dados (mocks). Então dispare análise:

POST /api/posts/<post_id>/analyze

Se o `CELERY_BROKER_URL` estiver configurado, a tarefa será enfileirada. Caso contrário, roda sincronamente.

4. Exemplos de endpoints úteis:
- `GET /api/accounts?user_id=1`
- `GET /api/accounts/<id>/analytics`
- `POST /api/ml/train` (cria experimento stub)

5. Próximos passos para aprendizado interativo:
- Criar notebooks com exemplos reais de análise de texto usando `SentimentService`.
- Implementar um modelo simples (ex.: Naive Bayes) para classificar comentários.
- Experimentar com métricas e salvar runs via `/api/ml/experiments`.
