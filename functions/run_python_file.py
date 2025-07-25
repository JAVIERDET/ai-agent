"""
run_python_file.py
"""

import subprocess
from pathlib import Path

from google.genai import types

from config import EX_TIMEOUT
from functions.utils import (
    _create_abs_path,
    _check_suffix,
    _check_is_within_the_scope
)

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Run a python file within the current diretory. Returns an error" \
        "string if any or a string indicating the succesful execution",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "w_dir": types.Schema(
                type=types.Type.STRING,
                description="The working directory"
            ),
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The name of the python file to be run"
            ),
        },
    ),
)

def run_python_file(
        w_dir: str,
        file_path: str,
    ) -> str:
    """
    Run a python file within the current diretory
    
    Params:
        - w_dir: The current working directory
        - file_path: The name of the python file to be run
    
    Return: An error string if any or a string indicating the succesful
    execution
    """

    # Check file is within the scope
    err = _check_is_within_the_scope(file_path, w_dir, "execute")
    if err:
        return err

    # Tranform into Path objects
    w_dir: Path = Path(w_dir)
    file_path: Path = Path(file_path)

    # Join
    full_path = _create_abs_path(w_dir, file_path)

    # Raise an error if the full path does not point to an existing file
    if not full_path.exists():
        return f'Error: File "{full_path.name}" not found.'

    # Check suffix
    err = _check_suffix(full_path, ".py")
    if err:
        return err

    # Execute the file
    command = ["uv", "run", f"{full_path}"]
    try:
        ex_output = subprocess.run(
            command,
            capture_output=True,
            cwd=w_dir,
            timeout=EX_TIMEOUT,
            check=True
        )

    except Exception as exc:
        return f"Error: executing Python file: {exc}"

    # Return the formatted output
    output = []
    output.append(f"STDOUT: {ex_output.stdout}")
    output.append(f"STDERR: {ex_output.stderr}")
    output.append(
        "Process exited with code X" if ex_output.check_returncode() else ""
    )
    output.append("No output produced." if not ex_output else "")

    return "\n".join(output)
