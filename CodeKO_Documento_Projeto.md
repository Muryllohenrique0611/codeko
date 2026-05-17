# 🥊 CodeKO — Documento de Projeto

> Plataforma gamificada de aprendizado de T.I. com temática de boxe e souls-like

---

## 1. Visão Geral

**CodeKO** é uma plataforma web de aprendizado de programação e fundamentos de T.I., inspirada no modelo progressivo do Duolingo, com gamificação temática de boxe (Hajime no Ippo) e elementos de souls-like. O usuário é um **boxeador** que evolui através de módulos de conhecimento, enfrenta chefões, disputa rankings e pode conquistar o cinturão.

---

## 2. Plataforma e Arquitetura

- **Interface:** Web (site responsivo)
- **Backend:** Python com Flask
- **Arquitetura:** API-first (REST) — permite migração futura para app mobile/desktop sem reescrever o backend
- **Autenticação:** Login com Google (OAuth)
- **Banco de questões:** Fixo no lançamento (criado manualmente + auxílio de IAs gratuitas); integração com API de IA generativa em versões futuras

```
[Backend Python/Flask] ← API REST → [Site agora]
                                    [App mobile futuramente]
                                    [App desktop futuramente]
```

---

## 3. Estrutura de Níveis e Módulos

### 🟢 INICIANTE — "Fundamentos"

| # | Módulo | Conteúdo |
|---|--------|----------|
| 1 | Hardware & Software | Bits, bytes, binário, tipos de memória, sistemas operacionais |
| 2 | Lógica & Algoritmos | Fluxogramas, pseudocódigo, sequência, condição, repetição |
| 3 | Introdução ao Python | Variáveis, tipos (int, float, str, bool), print, input |
| 4 | Operadores | Aritméticos, lógicos, comparação, precedência |

### 🟡 INTERMEDIÁRIO — "Python na Prática"

| # | Módulo | Conteúdo |
|---|--------|----------|
| 5 | Estruturas de Controle | if/elif/else, operador ternário |
| 6 | Laços de Repetição | for, while, break, continue, range |
| 7 | Funções | def, return, parâmetros, escopo, recursão básica |
| 8 | Estruturas de Dados | Listas, tuplas, dicionários, sets |
| 9 | Introdução ao Big O | O(1), O(n), O(n²) — conceito e exemplos simples |

### 🔴 PRO — "Pensamento Computacional"

| # | Módulo | Conteúdo |
|---|--------|----------|
| 10 | Big O Avançado | O(log n), O(n log n), análise de algoritmos reais |
| 11 | POO em Python | Classes, objetos, herança, encapsulamento, polimorfismo |
| 12 | Algoritmos Clássicos | Busca linear/binária, bubble sort, merge sort |
| 13 | Tratamento de Erros | try/except, exceções customizadas, boas práticas |
| 14 | Recapitulação Geral | Mix de todos os módulos — gate para o cinturão |

> **Total estimado de questões no lançamento:** ~210 (15 por módulo)

---

## 4. Progressão de Nível

```
✅ Completa todos os módulos INICIANTE
            ↓
📝 Recapitulação geral INICIANTE → INTERMEDIÁRIO
            ↓
✅ Completa todos os módulos INTERMEDIÁRIO
            ↓
📝 Recapitulação geral INTERMEDIÁRIO → PRO
            ↓
✅ Completa todos os módulos PRO
            ↓
🥊 Apto para disputar o CINTURÃO
```

- Questões básicas podem reaparecer em níveis superiores como revisão
- A recapitulação cobre **todos os módulos já vistos** do nível

---

## 5. Tipos de Questão

### Questões Teóricas (todos os níveis)
- **Múltipla escolha** — 4 alternativas
- **Verdadeiro ou Falso**

### Questões de Código (a partir do módulo de Python)
- **Múltipla escolha com trechos de código** — selecionar o trecho correto
- **Complete a lacuna** — usuário digita a parte faltante do código

### Execução ao Vivo
Após responder questões de código, o app **executa o código completo** e exibe o resultado em tempo real com animação de terminal.

```python
# Exemplo de questão com lacuna:
"____range(0,10):
     print("{}".format(i))"
# Usuário preenche: "for i in"
# App monta e executa o código completo, mostrando o output
```

> **Execução segura:** Sandbox via `subprocess` ou `RestrictedPython` para evitar código malicioso

---

## 6. Tarefa Diária

- **10 questões por dia**, até **00h** do dia corrente
- Composição: **7 questões do módulo atual + 3 de módulos anteriores**
- Questões erradas devem ser refeitas ao final da sessão antes de concluir
- Resultado registrado na ficha do lutador

---

## 7. Ficha do Lutador (Perfil)

Cada usuário tem uma ficha inspirada nas fichas de boxeadores do Ippo:

```
⚔️  [Nome do Usuário]
Categoria: Intermediário 🟡

Lutas:      10   (total de tarefas realizadas)
Vitórias:    7   (tarefas completas com algum erro)
Nocautes:    3   (tarefas perfeitas, sem nenhum erro)
Derrotas:    3   (tarefas não realizadas no dia)
```

Além disso, o perfil exibe:
- 📊 Histórico de batalhas
- 📈 Gráfico de evolução de XP
- 🏅 Conquistas desbloqueadas

---

## 8. Sistema de XP e Ranking

### Tabela de XP

| Ação | XP |
|------|----|
| 🥊 Vitória (tarefa feita com erros) | +100 XP |
| 💥 Nocaute (tarefa perfeita) | +150 XP |
| 💀 Derrota (não fez a tarefa) | -50 XP |
| 😤 Ressurreição aprovada (+60%) | +250 XP |
| 💣 Ressurreição reprovada (-60%) | -100 XP |
| 👑 Ganhou o cinturão | +500 XP |
| 😞 Perdeu disputa do cinturão | -150 XP |

### Ranking
- Usuários são ranqueados por XP total dentro de cada categoria (Iniciante / Intermediário / Pro)
- Não fazer a tarefa diária → perde o combo/streak → cai posições no ranking
- Apenas jogadores **PRO** participam da disputa pelo cinturão

---

## 9. Mecânica de Recuperação — "Desafio de Ressurreição"

Perdeu 1 dia sem fazer a tarefa? Pode ativar o Desafio de Ressurreição:

```
15 questões — tudo que o usuário já viu
        ├── ✅ +60% de aproveitamento (9/15 ou mais)
        │       └── Mata os 2 dias perdidos + bônus +250 XP
        │           MAS perde o direito de desafiar o cinturão naquela semana
        └── ❌ -60% de aproveitamento (menos de 9/15)
                └── Perde o DOBRO do que perderia só por não ter feito as tarefas
```

- Pode ser usado **apenas 1 vez por semana**
- Quem usa o Desafio de Ressurreição **perde o direito ao desafio do cinturão** na mesma semana

---

## 10. Sistema do Cinturão 🏆

### Quem pode desafiar
- Apenas os **Top 3 jogadores PRO** do ranking podem desafiar o cinturão
- Apenas **1 desafio por semana**

### Como funciona a disputa
- **10 questões simultâneas** — desafiante e campeão respondem ao mesmo tempo
- **15 segundos por questão**
- Questões variadas com foco nas avançadas
- Quem acertar mais vence e conquista (ou mantém) o cinturão

### Resultados da disputa
| Resultado | Consequência |
|-----------|-------------|
| Desafiante vence | Toma o cinturão + +500 XP |
| Campeão defende | Mantém o cinturão |
| Desafiante perde | Cai no ranking + -150 XP |

### Defesa solo do campeão
Se **ninguém desafiar** o campeão na semana:
- Campeão enfrenta **10 questões sozinho**
- Precisa de **70% de aproveitamento** (7/10) para manter o cinturão
- Se não atingir 70%, o cinturão fica **vago** — qualquer Top 3 pode assumir fazendo o mesmo esquema

### Penalidade de inatividade do Top 1
- Se o **Top 1 PRO não realizar o desafio do cinturão** na semana → cai automaticamente para o **3º lugar**

---

## 11. Animações e Visual

- **Estilo:** Anime/mangá, dinâmico, simples e limpo — inspirado em Hajime no Ippo
- **Paleta:** Cores vibrantes com tema de boxe, sem exageros

### Animações do Boxeador (durante execução de código)
| Animação | Momento |
|----------|---------|
| 👊 Soco no saco de pancada | Executando o código |
| 🏃 Pulando corda / correndo | Carregando questão |
| 😤 Respirando fundo | Aguardando resposta do usuário |
| 💪 Braço erguido / comemorando | Resposta correta |
| 😵 Levando um soco | Resposta errada |
| 🧘 Meditando / focado | Entre módulos |

- Animações feitas em **CSS puro + SVG** — leve, sem imagens externas
- Seleção **aleatória** entre as animações disponíveis

---

## 12. Roadmap — Versões Futuras

| Versão | Funcionalidade |
|--------|---------------|
| v1.0 | MVP — módulos, questões fixas, ranking, cinturão |
| v1.5 | Chefões por módulo (questão final difícil) |
| v2.0 | Integração com API de IA para questões dinâmicas |
| v2.5 | Mensagens de dica deixadas por outros usuários |
| v3.0 | App mobile (React Native ou Flutter) |
| v3.5 | Novos temas além de Python (JavaScript, Java, etc.) |

---

## 13. Stack Técnica

| Componente | Tecnologia |
|------------|-----------|
| Backend | Python + Flask |
| Banco de Dados | PostgreSQL ou SQLite (MVP) |
| Autenticação | Google OAuth |
| Frontend | HTML + CSS + JavaScript |
| Execução de Código | subprocess / RestrictedPython (sandbox) |
| Hospedagem | Railway ou Render (gratuito para MVP) |
| Animações | CSS Animations + SVG |

---

*Documento gerado após sessão de alinhamento — CodeKO v0.1*
