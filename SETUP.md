# CodeKO - Setup Guide

## Instalação

### 1. Clonar o repositório
```bash
git clone <repo-url>
cd codeko
```

### 2. Criar ambiente virtual
```bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
```

### 3. Instalar dependências
```bash
pip install -r requirements.txt
```

### 4. Configurar Google OAuth

#### a. Criar aplicação no Google Cloud Console
1. Acessar https://console.cloud.google.com
2. Criar um novo projeto (ex: "CodeKO")
3. Ir para "APIs & Services" → "Library"
4. Procurar "Google+ API" e habilitar
5. Ir para "Credentials" → "Create Credentials" → "OAuth 2.0 Client ID"
6. Escolher "Web application"
7. Adicionar authorized redirect URIs:
   - `http://localhost:5000/auth/callback`
   - `https://seu-dominio.com/auth/callback` (em produção)

#### b. Copiar credenciais
1. Copiar `Client ID` e `Client Secret`
2. Criar arquivo `.env` na raiz do projeto:
```bash
cp .env.example .env
```

3. Editar `.env` e adicionar as credenciais:
```env
GOOGLE_CLIENT_ID=seu_client_id_aqui
GOOGLE_CLIENT_SECRET=seu_client_secret_aqui
FLASK_ENV=development
SECRET_KEY=sua_chave_secreta_aqui
```

### 5. Inicializar banco de dados
```bash
python seed.py
```

### 6. Rodar a aplicação
```bash
python run.py
```

A aplicação estará disponível em `http://localhost:5000`

---

## Estrutura do Projeto

```
codeko/
├── app/
│   ├── templates/          # Templates HTML
│   ├── routes/             # Blueprints Flask (auth, main, api)
│   ├── models/             # Modelos SQLAlchemy
│   └── __init__.py         # Factory da app Flask
├── config/
│   └── settings.py         # Configurações
├── seed.py                 # Script para popular DB
├── run.py                  # Entrada da aplicação
├── requirements.txt        # Dependências
└── .env.example            # Template de variáveis de ambiente
```

## API Endpoints

### Autenticação
- `GET /auth/login` — Inicia OAuth com Google
- `GET /auth/callback` — Callback do Google
- `GET /auth/logout` — Logout

### Principal
- `GET /` — Landing page
- `GET /home` — Dashboard (requer autenticação)
- `GET /modules` — Lista de módulos
- `GET /quiz/<module_id>` — Quiz do módulo

### API (JSON)
- `GET /api/user/profile` — Dados do usuário
- `GET /api/modules` — Módulos da categoria
- `GET /api/questions?module_id=X&limit=10` — Questões
- `GET /api/ranking/<category>` — Ranking por categoria
- `POST /api/progress/submit` — Submeter resultado da tarefa

---

## Desenvolvimento

### Adicionar novas questões
Editar `seed.py` e adicionar questões no dicionário `questions`.
Tipos suportados:
- `multiple_choice` — Múltipla escolha
- `true_false` — Verdadeiro/Falso
- `code_gap` — Preencher lacuna em código

### Rodar testes (futuro)
```bash
pytest tests/
```

---

## Troubleshooting

**"ModuleNotFoundError: No module named 'flask_sqlalchemy'"**
```bash
pip install flask flask-sqlalchemy flask-login oauthlib requests
```

**"GOOGLE_CLIENT_ID not found"**
- Verifique se `.env` existe na raiz do projeto
- Verifique se as variáveis estão corretas

**"Redirect URI mismatch"**
- Verifique se `http://localhost:5000/auth/callback` está nas authorized URIs
- Se em produção, adicione o domínio correto

---

## Licença

MIT
