"""
get_file_content.py
"""

from pathlib import Path
from google.genai import types

from functions.utils import (
    _check_is_file,
    _check_is_within_the_scope,
    _create_abs_path
)

from config import MAX_LENGTH_LIM

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Gets the content of a file and returns it as a string. It is" \
        "constrained to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "w_dir": types.Schema(
                type=types.Type.STRING,
                description="The working directory"
            ),
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path of the file which its content its " \
                    "intended to be obtained"
            ),
        },
    ),
)


def get_file_content(
        w_dir:str,
        file_path:str
        ) -> str:
    """
    Get the content of a file and return it as a string
    """

    # Check scope
    err = _check_is_within_the_scope(file_path, w_dir)
    if err is not None:
        return err

    # Transform to path variables
    w_dir: Path = Path(w_dir)
    file_path: Path = Path(file_path)

    # Create absolute path
    final_path = _create_abs_path(w_dir, file_path)

    # Check it is a file
    err = _check_is_file(final_path)
    if err is not None:
        return err

    # Read file
    try:
        file_str = final_path.read_text(encoding='utf-8')
    except Exception as exc:
        return f"Error: {err}"

    # Return only the last MAX_LENGTH_LIM characters
    if len(file_str) <= MAX_LENGTH_LIM:
        return file_str

    return f'{file_str[:-MAX_LENGTH_LIM]} [...File "{file_path}" truncated at 10000 characters].'
