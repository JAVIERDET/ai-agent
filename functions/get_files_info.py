"""
get_files_info.py
"""

from google.genai import types
from pathlib import Path

from functions.utils import (
    _check_is_dir,
    _check_is_within_the_scope,
    _create_abs_path
)

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes," \
        " constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "w_dir": types.Schema(
                type=types.Type.STRING,
                description="The working directory"
            ),
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the "\
                    "working directory. If not provided, lists files in the working "\
                        "directory itself.",
            ),
        },
    ),
)


def get_files_info(
        w_dir:str,
        directory: str
        ) -> str:
    """
    List all the items within a directory in the next fashion:
        Ex:
        - README.md: file_size=1032 bytes, is_dir=False
        - src: file_size=128 bytes, is_dir=True
        - package.json: file_size=1234 bytes, is_dir=False
    """

    # Check tha directory is given
    if directory is None:
        return f"Error: Directory not set: {directory}"

    # Transform to paths
    dir_path = Path(directory)
    w_dir_path = Path(w_dir)

    # Create absolute path
    final_path = _create_abs_path(w_dir_path, dir_path)

    # Check if the joined path is a directory
    err =  _check_is_dir(final_path)
    if err is not None:
        return err

    # Check full directoy is within_working directory scope
    err = _check_is_within_the_scope(final_path, w_dir_path)
    if err is not None:
        return err

    # Create a list of file strings info
    info_list: list = []
    for item in final_path.iterdir():
        try:
            size = item.stat().st_size
            info_list.append(
                f"- {item.name}: file_size={size} bytes, is_dir={item.is_dir()}"
            )
        except Exception as err:
            return f"Error: {err}"

    # Return the data as a string:
    return "\n".join(info_list)
