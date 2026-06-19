# 🥊 CodeKO - Quick Start

## 🎯 O que é CodeKO?

**CodeKO** é uma plataforma gamificada de aprendizado de programação e T.I. com temática de boxe (inspirada em Hajime no Ippo). Você é um boxeador que evolui através de módulos, enfrenta chefões e disputa um cinturão digital.

## 🚀 Iniciar a aplicação

```bash
cd d:\python\Projeto\codeko
python run.py
```

Depois acesse: **http://localhost:5000**

## 📋 O que você verá

1. **Landing Page** → Clique em "Começar Agora"
2. **Login** → Clique em "Entrar com Google"
3. **Dashboard** → Seu perfil com XP, categoria, estatísticas
4. **Módulos** → Escolha um módulo para responder questões
5. **Quiz** → Responda as 10 questões do dia
6. **Code Executor** → Teste código Python de forma segura
7. **Ranking** → Acompanhe sua posição global

## 📁 Estrutura do Projeto

```
codeko/
├── app/
│   ├── templates/          # Páginas HTML (6 templates)
│   ├── routes/             # API e rotas Flask
│   ├── models/             # Modelos do banco de dados
│   ├── utils/              # Code Executor (sandbox)
│   └── __init__.py         # Factory da app Flask
├── config/
│   └── settings.py         # Configurações e variáveis
├── tests/
│   └── test_code_executor.py  # Testes do sandbox
├── seed.py                 # Script para popular DB com 210 questões
├── run.py                  # Entrada da aplicação
├── requirements.txt        # Dependências
├── .env                    # Credenciais (NÃO fazer commit!)
├── .env.example            # Template de .env
└── .gitignore              # Arquivos ignorados
```

## ✅ Status do Projeto

### Implementado
- ✅ **210 questões** (14 módulos × 15 questões)
- ✅ **6 páginas HTML** responsivas com tema de boxe
- ✅ **Autenticação Google OAuth** 2.0
- ✅ **Code Executor** seguro com sandbox e timeout
- ✅ **Sistema de XP e Ranking** (pronto para usar)
- ✅ **Proteção contra vulnerabilidades** (CSRF, SQL Injection)
- ✅ **API REST** completa para frontend/mobile

### Próximas Fases
- [ ] Desafio de Ressurreição (recuperar dias perdidos)
- [ ] Disputa pelo Cinturão (Top 3 PRO)
- [ ] Histórico de batalhas detalhado
- [ ] Deploy em produção (Railway/Render)

## 🔒 Segurança

**Correções Aplicadas:**
- ✅ Removido `debug=True` (configurável por env)
- ✅ Desabilitado `OAUTHLIB_INSECURE_TRANSPORT` em produção
- ✅ Validação obrigatória de `SECRET_KEY`
- ✅ Proteção CSRF com Flask-WTF
- ✅ SQL Injection prevenido com SQLAlchemy ORM

**Code Executor:**
- ✅ Sandbox isolado com subprocess
- ✅ Timeout de 5 segundos (evita loops infinitos)
- ✅ Validação de código antes de executar
- ✅ Bloqueio de imports perigosos (os, subprocess, socket)

## 📊 Tipos de Questões

1. **Múltipla Escolha** — Selecione a resposta correta (4 opções)
2. **Verdadeiro/Falso** — Teste seu conhecimento teórico
3. **Complete a Lacuna** — Preencha o código faltante
4. **Execução ao Vivo** — Seu código é executado em tempo real

## 🏆 Sistema de Gamificação

### XP por Ação
- 💥 **Nocaute (100%)**: +150 XP
- ✅ **Vitória (60%+)**: +100 XP  
- ❌ **Derrota (<60%)**: -50 XP
- 🔥 **Combo Bonus**: +5 XP por dia consecutivo

### Ficha do Lutador
```
⚔️  [Seu Nome]
Categoria: Iniciante 🟢

Lutas:     10
Vitórias:   7
Nocautes:   3
Derrotas:   3
```

### Ranking
- 🥇 Top 1 é o campeão
- 📈 Ordenado por XP total
- 🏅 Separado por categoria (Iniciante / Intermediário / PRO)

## 🧪 Testar Code Executor

```bash
# Dentro do projeto
python -c "
from app.utils import CodeExecutor

# Teste simples
result = CodeExecutor.execute(\"print('Hello!')\")
print(result)
# Output: {'success': True, 'output': 'Hello!', ...}

# Com timeout
result = CodeExecutor.execute('import time; time.sleep(10)', timeout=2)
print(result['status'])
# Output: 'timeout'
"
```

## 🔧 Configuração para Produção

### 1. Gerar nova SECRET_KEY
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### 2. Atualizar .env
```bash
FLASK_ENV=production
SECRET_KEY=<sua_nova_chave>
GOOGLE_CLIENT_ID=<seu_client_id>
GOOGLE_CLIENT_SECRET=<seu_client_secret>
DATABASE_URL=postgresql://user:pass@host/db
```

### 3. Deploy
- Use WSGI server (Gunicorn, uWSGI)
- Configure HTTPS obrigatório
- Use variáveis de ambiente do servidor
- Ative logging e monitoring

## 📚 Módulos Disponíveis

### 🟢 Iniciante (Hardware & Fundamentos)
1. Hardware & Software
2. Lógica & Algoritmos
3. Introdução ao Python
4. Operadores

### 🟡 Intermediário (Python na Prática)
5. Estruturas de Controle
6. Laços de Repetição
7. Funções
8. Estruturas de Dados
9. Introdução ao Big O

### 🔴 PRO (Pensamento Computacional)
10. Big O Avançado
11. POO em Python
12. Algoritmos Clássicos
13. Tratamento de Erros
14. Recapitulação Geral (Gate para cinturão)

## 🤝 Contribuir

Quer adicionar novas questões? Edite `seed.py`:

```python
{
    "module_number": 1,
    "type": "multiple_choice",  # ou true_false, code_gap
    "level": "iniciante",
    "lang": "pt",
    "statement": "Qual é a menor unidade...",
    "code_snippet": None,  # Apenas para code_gap
    "correct_answer": "bit",
    "options": json.dumps(["bit", "byte", "kilobyte", "nibble"]),
    "explanation": "O bit (binary digit)...",
}
```

Depois execute:
```bash
python seed.py
```

## 📞 Troubleshooting

**"GOOGLE_CLIENT_ID not found"**
- Verifique se `.env` existe na raiz
- Configure as credenciais do Google Cloud Console

**"Code execution timeout"**
- Normal! Loops infinitos são interrompidos após 5 segundos

**"Porta 5000 em uso"**
```bash
# Mude para outra porta
FLASK_PORT=5001 python run.py
```

## 📝 Licença

MIT - Desenvolvido com ❤️ para boxeadores da programação

---

**Status:** v1.0-beta | **Last Updated:** 19/06/2026
