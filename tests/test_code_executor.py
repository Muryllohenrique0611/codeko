"""Testes para o Code Executor."""

from app.utils import CodeExecutor


def test_execute_simple_code():
    """Testa execução de código simples."""
    code = "print('Hello, World!')"
    result = CodeExecutor.execute(code)

    assert result["success"] is True
    assert "Hello, World!" in result["output"]
    assert result["status"] == "success"
    print("✅ test_execute_simple_code PASSOU")


def test_execute_with_loop():
    """Testa execução com loop."""
    code = """
for i in range(3):
    print(i)
"""
    result = CodeExecutor.execute(code)

    assert result["success"] is True
    assert "0" in result["output"]
    assert "2" in result["output"]
    print("✅ test_execute_with_loop PASSOU")


def test_timeout():
    """Testa se timeout funciona."""
    code = "while True: pass"
    result = CodeExecutor.execute(code, timeout=2)

    assert result["success"] is False
    assert result["status"] == "timeout"
    assert "tempo limite" in result["error"].lower()
    print("✅ test_timeout PASSOU")


def test_syntax_error():
    """Testa se detecta erro de sintaxe."""
    code = "print('unclosed string"
    result = CodeExecutor.execute(code)

    assert result["success"] is False
    assert result["status"] == "error"
    print("✅ test_syntax_error PASSOU")


def test_validate_forbidden():
    """Testa validação de código perigoso."""
    code = "import os; os.system('ls')"
    validation = CodeExecutor.validate_code(code)

    assert validation["valid"] is False
    assert len(validation["warnings"]) > 0
    print("✅ test_validate_forbidden PASSOU")


def test_validate_safe():
    """Testa validação de código seguro."""
    code = "print('safe code')"
    validation = CodeExecutor.validate_code(code)

    assert validation["valid"] is True
    assert len(validation["warnings"]) == 0
    print("✅ test_validate_safe PASSOU")


def test_execute_with_input():
    """Testa execução com input."""
    code = """
name = input()
print(f'Olá, {name}!')
"""
    result = CodeExecutor.execute_with_input(code, test_input="João")

    assert result["success"] is True
    assert "João" in result["output"]
    print("✅ test_execute_with_input PASSOU")


def test_runtime_error():
    """Testa detecção de erro em tempo de execução."""
    code = """
lista = [1, 2, 3]
print(lista[10])
"""
    result = CodeExecutor.execute(code)

    assert result["success"] is False
    assert result["status"] == "error"
    print("✅ test_runtime_error PASSOU")


if __name__ == "__main__":
    print("🧪 Executando testes do Code Executor...\n")

    test_execute_simple_code()
    test_execute_with_loop()
    test_timeout()
    test_syntax_error()
    test_validate_forbidden()
    test_validate_safe()
    test_execute_with_input()
    test_runtime_error()

    print("\n✅ Todos os testes passaram!")
