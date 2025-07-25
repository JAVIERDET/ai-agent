"""
write_file.py
"""

from google.genai import types
from pathlib import Path

from functions.utils import (
    _check_is_dir,
    _check_is_within_the_scope,
    _create_abs_path
)


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Ovewrites the file contents with the 'content' string variable." \
        "COnstrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "w_dir": types.Schema(
                type=types.Type.STRING,
                description="The working directory"
            ),
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The name of the file to be overwritten"
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write on the file"
            ),
        },
    ),
)


def write_file(
        w_dir:str,
        file_path:str,
        content:str
        ) -> str:
    """
    Ovewrite the file contents with the 'content' string variable.
    """

    # Transform to paths
    w_dir: Path = Path(w_dir)
    file_path: Path = Path(file_path)

    # Create absolute path
    final_path = _create_abs_path(w_dir, file_path)

    # Check full directoy is within_working directory scope
    err = _check_is_within_the_scope(final_path, w_dir, "write")
    if err is not None:
        return err

    # Create file if it does not exists
    try:
        final_path.touch()

    except Exception as exc:
        return f"Error: {exc}"

    # Overwrite content
    try:
        final_path.write_text(content)
    except Exception as exc:
        f"Error: {exc}"

    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
