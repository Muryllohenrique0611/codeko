"""
Script para popular o banco de dados com módulos e questões.
Execute: python seed.py
"""

from app import create_app, db
from app.models import Module, Question
import json

app = create_app()


def seed_modules():
    modules = [
        # INICIANTE
        {"number": 1, "name": "Hardware & Software",      "description": "Bits, bytes, binário, tipos de memória e sistemas operacionais", "category": "iniciante",     "order": 1},
        {"number": 2, "name": "Lógica & Algoritmos",      "description": "Fluxogramas, pseudocódigo, sequência, condição e repetição",      "category": "iniciante",     "order": 2},
        {"number": 3, "name": "Introdução ao Python",     "description": "Variáveis, tipos, print e input",                                  "category": "iniciante",     "order": 3},
        {"number": 4, "name": "Operadores",               "description": "Aritméticos, lógicos, comparação e precedência",                   "category": "iniciante",     "order": 4},
        # INTERMEDIÁRIO
        {"number": 5, "name": "Estruturas de Controle",   "description": "if, elif, else e operador ternário",                               "category": "intermediario", "order": 5},
        {"number": 6, "name": "Laços de Repetição",       "description": "for, while, break, continue e range",                              "category": "intermediario", "order": 6},
        {"number": 7, "name": "Funções",                  "description": "def, return, parâmetros, escopo e recursão básica",                 "category": "intermediario", "order": 7},
        {"number": 8, "name": "Estruturas de Dados",      "description": "Listas, tuplas, dicionários e sets",                               "category": "intermediario", "order": 8},
        {"number": 9, "name": "Introdução ao Big O",      "description": "O(1), O(n), O(n²) — conceito e exemplos simples",                  "category": "intermediario", "order": 9},
        # PRO
        {"number": 10, "name": "Big O Avançado",          "description": "O(log n), O(n log n) e análise de algoritmos reais",               "category": "pro",           "order": 10},
        {"number": 11, "name": "POO em Python",           "description": "Classes, objetos, herança, encapsulamento e polimorfismo",          "category": "pro",           "order": 11},
        {"number": 12, "name": "Algoritmos Clássicos",    "description": "Busca linear/binária, bubble sort e merge sort",                   "category": "pro",           "order": 12},
        {"number": 13, "name": "Tratamento de Erros",     "description": "try/except, exceções customizadas e boas práticas",                 "category": "pro",           "order": 13},
        {"number": 14, "name": "Recapitulação Geral",     "description": "Mix de todos os módulos — gate para o cinturão",                   "category": "pro",           "order": 14},
    ]

    for m in modules:
        exists = Module.query.filter_by(number=m["number"]).first()
        if not exists:
            db.session.add(Module(**m))

    db.session.commit()
    print(f"✅ {len(modules)} módulos inseridos.")


def seed_questions():
    questions = [

        # ══════════════════════════════════════════
        # MÓDULO 1 — Hardware & Software (15 questões)
        # ══════════════════════════════════════════

        {
            "module_number": 1,
            "type": "multiple_choice",
            "level": "iniciante",
            "lang": "pt",
            "statement": "Qual é a menor unidade de informação em um computador?",
            "code_snippet": None,
            "correct_answer": "bit",
            "options": json.dumps(["bit", "byte", "kilobyte", "nibble"]),
            "explanation": "O bit (binary digit) é a menor unidade de informação, podendo ser 0 ou 1.",
        },
        {
            "module_number": 1,
            "type": "multiple_choice",
            "level": "iniciante",
            "lang": "pt",
            "statement": "Quantos bits formam 1 byte?",
            "code_snippet": None,
            "correct_answer": "8",
            "options": json.dumps(["4", "8", "16", "32"]),
            "explanation": "1 byte é composto por 8 bits.",
        },
        {
            "module_number": 1,
            "type": "true_false",
            "level": "iniciante",
            "lang": "pt",
            "statement": "A memória RAM é um tipo de memória volátil, ou seja, perde seus dados quando o computador é desligado.",
            "code_snippet": None,
            "correct_answer": "verdadeiro",
            "options": json.dumps(["verdadeiro", "falso"]),
            "explanation": "A RAM (Random Access Memory) é volátil — seus dados são apagados sem energia.",
        },
        {
            "module_number": 1,
            "type": "multiple_choice",
            "level": "iniciante",
            "lang": "pt",
            "statement": "O que é o HD (Hard Disk) de um computador?",
            "code_snippet": None,
            "correct_answer": "Memória secundária de armazenamento permanente",
            "options": json.dumps([
                "Memória principal de acesso rápido",
                "Memória secundária de armazenamento permanente",
                "Processador responsável pelos cálculos",
                "Componente de entrada e saída de dados"
            ]),
            "explanation": "O HD é uma memória secundária não volátil, usada para armazenamento permanente de dados.",
        },
        {
            "module_number": 1,
            "type": "multiple_choice",
            "level": "iniciante",
            "lang": "pt",
            "statement": "Qual componente é conhecido como o 'cérebro' do computador?",
            "code_snippet": None,
            "correct_answer": "CPU",
            "options": json.dumps(["RAM", "CPU", "GPU", "SSD"]),
            "explanation": "A CPU (Central Processing Unit) é o processador principal, responsável por executar instruções.",
        },
        {
            "module_number": 1,
            "type": "true_false",
            "level": "iniciante",
            "lang": "pt",
            "statement": "Software é o conjunto de componentes físicos do computador, como placa-mãe e processador.",
            "code_snippet": None,
            "correct_answer": "falso",
            "options": json.dumps(["verdadeiro", "falso"]),
            "explanation": "Software são programas e dados (intangíveis). Hardware são os componentes físicos.",
        },
        {
            "module_number": 1,
            "type": "multiple_choice",
            "level": "iniciante",
            "lang": "pt",
            "statement": "Qual é a representação do número decimal 2 em binário?",
            "code_snippet": None,
            "correct_answer": "10",
            "options": json.dumps(["01", "10", "11", "100"]),
            "explanation": "O número 2 em binário é 10, pois 1×2¹ + 0×2⁰ = 2.",
        },
        {
            "module_number": 1,
            "type": "multiple_choice",
            "level": "iniciante",
            "lang": "pt",
            "statement": "O que é um Sistema Operacional?",
            "code_snippet": None,
            "correct_answer": "Software que gerencia os recursos do hardware e serve de base para outros programas",
            "options": json.dumps([
                "Um tipo de processador mais moderno",
                "Software que gerencia os recursos do hardware e serve de base para outros programas",
                "A memória principal do computador",
                "Um programa para navegar na internet"
            ]),
            "explanation": "O SO (ex: Windows, Linux) gerencia hardware e fornece serviços para os demais softwares.",
        },
        {
            "module_number": 1,
            "type": "multiple_choice",
            "level": "iniciante",
            "lang": "pt",
            "statement": "Quantos bytes equivalem a 1 Kilobyte (KB)?",
            "code_snippet": None,
            "correct_answer": "1024",
            "options": json.dumps(["100", "1000", "1024", "2048"]),
            "explanation": "1 KB = 1024 bytes, pois computadores usam base binária (2¹⁰ = 1024).",
        },
        {
            "module_number": 1,
            "type": "true_false",
            "level": "iniciante",
            "lang": "pt",
            "statement": "A memória cache é mais lenta que a memória RAM.",
            "code_snippet": None,
            "correct_answer": "falso",
            "options": json.dumps(["verdadeiro", "falso"]),
            "explanation": "A memória cache é mais rápida que a RAM, ficando entre o processador e a RAM para acelerar o acesso.",
        },
        {
            "module_number": 1,
            "type": "multiple_choice",
            "level": "iniciante",
            "lang": "pt",
            "statement": "Qual é a representação binária do número decimal 5?",
            "code_snippet": None,
            "correct_answer": "101",
            "options": json.dumps(["100", "101", "110", "011"]),
            "explanation": "5 em binário é 101: 1×2² + 0×2¹ + 1×2⁰ = 4+0+1 = 5.",
        },
        {
            "module_number": 1,
            "type": "multiple_choice",
            "level": "iniciante",
            "lang": "pt",
            "statement": "O que diferencia um SSD de um HD tradicional?",
            "code_snippet": None,
            "correct_answer": "O SSD usa memória flash sem partes móveis, sendo mais rápido",
            "options": json.dumps([
                "O SSD tem maior capacidade de armazenamento",
                "O SSD usa memória flash sem partes móveis, sendo mais rápido",
                "O SSD é um tipo de memória RAM",
                "O SSD é mais barato que o HD"
            ]),
            "explanation": "SSDs usam chips de memória flash, sem partes mecânicas, tornando-os muito mais rápidos.",
        },
        {
            "module_number": 1,
            "type": "true_false",
            "level": "iniciante",
            "lang": "pt",
            "statement": "Um programa de computador é considerado hardware.",
            "code_snippet": None,
            "correct_answer": "falso",
            "options": json.dumps(["verdadeiro", "falso"]),
            "explanation": "Programas são software. Hardware são os componentes físicos como teclado, placa de vídeo etc.",
        },
        {
            "module_number": 1,
            "type": "multiple_choice",
            "level": "iniciante",
            "lang": "pt",
            "statement": "Qual das opções abaixo é um exemplo de dispositivo de ENTRADA?",
            "code_snippet": None,
            "correct_answer": "Teclado",
            "options": json.dumps(["Monitor", "Impressora", "Teclado", "Caixa de som"]),
            "explanation": "Dispositivos de entrada enviam dados ao computador. O teclado é o exemplo mais clássico.",
        },
        {
            "module_number": 1,
            "type": "multiple_choice",
            "level": "iniciante",
            "lang": "pt",
            "statement": "O número binário 1010 equivale a qual número decimal?",
            "code_snippet": None,
            "correct_answer": "10",
            "options": json.dumps(["8", "9", "10", "12"]),
            "explanation": "1010 em binário: 1×2³ + 0×2² + 1×2¹ + 0×2⁰ = 8+0+2+0 = 10.",
        },

    ]

    modules_map = {m.number: m.id for m in Module.query.all()}

    count = 0
    for q in questions:
        module_id = modules_map.get(q["module_number"])
        if not module_id:
            print(f"⚠️  Módulo {q['module_number']} não encontrado, pulando questão.")
            continue

        exists = Question.query.filter_by(
            module_id=module_id,
            statement=q["statement"]
        ).first()

        if not exists:
            db.session.add(Question(
                module_id=module_id,
                type=q["type"],
                level=q["level"],
                statement=q["statement"],
                code_snippet=q.get("code_snippet"),
                correct_answer=q["correct_answer"],
                options=q["options"],
                explanation=q["explanation"],
            ))
            count += 1

    db.session.commit()
    print(f"✅ {count} questões inseridas.")


if __name__ == "__main__":
    with app.app_context():
        print("🥊 Iniciando seed do CodeKO...")
        seed_modules()
        seed_questions()
        print("🏆 Seed concluído com sucesso!")