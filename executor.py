"""
Python Code Snippet Executor Module
Executes Python code snippets in isolated sub-processes and formats terminal output.
"""

import sys
import subprocess
import time
import os

def run_python_snippet(code: str, timeout_seconds: float = 5.0) -> dict:
    """
    Executes a Python code string using the current Python virtual environment.
    Captures stdout, stderr, execution time, and exit code.
    """
    if not code or not code.strip():
        return {
            "success": False,
            "stdout": "",
            "stderr": "Nenhum código para executar.",
            "exit_code": -1,
            "execution_time_ms": 0.0
        }

    start_time = time.time()
    python_exe = sys.executable

    try:
        process = subprocess.run(
            [python_exe, "-c", code],
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
            env={**os.environ, "PYTHONUNBUFFERED": "1"}
        )
        elapsed_ms = (time.time() - start_time) * 1000

        return {
            "success": process.returncode == 0,
            "stdout": process.stdout,
            "stderr": process.stderr,
            "exit_code": process.returncode,
            "execution_time_ms": round(elapsed_ms, 2)
        }
    except subprocess.TimeoutExpired:
        elapsed_ms = (time.time() - start_time) * 1000
        return {
            "success": False,
            "stdout": "",
            "stderr": f"⏱️ Tempo limite excedido! (Mais de {timeout_seconds} segundos)",
            "exit_code": 124,
            "execution_time_ms": round(elapsed_ms, 2)
        }
    except Exception as e:
        elapsed_ms = (time.time() - start_time) * 1000
        return {
            "success": False,
            "stdout": "",
            "stderr": f"❌ Erro ao executar processo: {str(e)}",
            "exit_code": 1,
            "execution_time_ms": round(elapsed_ms, 2)
        }
