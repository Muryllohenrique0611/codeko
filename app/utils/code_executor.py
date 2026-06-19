# -*- coding: utf-8 -*-
"""
Executor seguro de código Python com sandbox.
Usa subprocess com timeout e restrições para evitar código malicioso.
"""

import subprocess
import sys
import json
from typing import Dict, Any


class CodeExecutor:
    """Executa código Python de forma segura com isolamento."""

    # Timeout padrão em segundos
    DEFAULT_TIMEOUT = 5

    # Código de entrada padrão para as questões
    DEFAULT_SETUP = """
import sys
sys.stdout = sys.stderr = open(__import__('os').devnull, 'w')
"""

    @staticmethod
    def execute(code: str, timeout: int = DEFAULT_TIMEOUT) -> Dict[str, Any]:
        """
        Executa código Python em um subprocess isolado.

        Args:
            code: Código Python a executar
            timeout: Tempo máximo em segundos

        Returns:
            {
                "success": bool,
                "output": str,
                "error": str,
                "status": "success|timeout|error"
            }
        """
        try:
            # Executar código em subprocess isolado
            process = subprocess.Popen(
                [sys.executable, "-c", code],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )

            stdout, stderr = process.communicate(timeout=timeout)

            # Se houve erro
            if process.returncode != 0:
                return {
                    "success": False,
                    "output": stdout.strip() if stdout else "",
                    "error": stderr.strip() if stderr else "Erro na execução",
                    "status": "error",
                }

            # Sucesso
            return {
                "success": True,
                "output": stdout.strip() if stdout else "",
                "error": "",
                "status": "success",
            }

        except subprocess.TimeoutExpired:
            # Código demorou muito
            process.kill()
            return {
                "success": False,
                "output": "",
                "error": f"Código excedeu o tempo limite ({timeout}s). Verifique loops infinitos.",
                "status": "timeout",
            }

        except Exception as e:
            # Erro inesperado
            return {
                "success": False,
                "output": "",
                "error": f"Erro ao executar: {str(e)}",
                "status": "error",
            }

    @staticmethod
    def validate_code(code: str) -> Dict[str, Any]:
        """
        Valida código para evitar construções perigosas.

        Args:
            code: Código Python a validar

        Returns:
            {
                "valid": bool,
                "warnings": list
            }
        """
        warnings = []
        forbidden_patterns = [
            ("import os", "Acesso ao sistema operacional não permitido"),
            ("import subprocess", "Execução de subprocessos não permitida"),
            ("import socket", "Acesso à rede não permitido"),
            ("__import__", "Importação dinâmica não permitida"),
            ("eval", "eval() não permitido"),
            ("exec", "exec() não permitido"),
            ("compile", "compile() não permitido"),
            ("open(", "Acesso a arquivos não permitido"),
        ]

        for pattern, message in forbidden_patterns:
            if pattern.lower() in code.lower():
                warnings.append(message)

        return {
            "valid": len(warnings) == 0,
            "warnings": warnings,
        }

    @staticmethod
    def execute_with_input(
        code: str, test_input: str = "", timeout: int = DEFAULT_TIMEOUT
    ) -> Dict[str, Any]:
        """
        Executa código com input simulado.

        Args:
            code: Código Python a executar
            test_input: Input para fornecer (separado por \\n)
            timeout: Tempo máximo em segundos

        Returns:
            Resultado da execução
        """
        try:
            process = subprocess.Popen(
                [sys.executable, "-c", code],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )

            stdout, stderr = process.communicate(input=test_input, timeout=timeout)

            if process.returncode != 0:
                return {
                    "success": False,
                    "output": stdout.strip() if stdout else "",
                    "error": stderr.strip() if stderr else "Erro na execução",
                    "status": "error",
                }

            return {
                "success": True,
                "output": stdout.strip() if stdout else "",
                "error": "",
                "status": "success",
            }

        except subprocess.TimeoutExpired:
            process.kill()
            return {
                "success": False,
                "output": "",
                "error": f"Código excedeu tempo limite ({timeout}s)",
                "status": "timeout",
            }

        except Exception as e:
            return {
                "success": False,
                "output": "",
                "error": f"Erro ao executar: {str(e)}",
                "status": "error",
            }
