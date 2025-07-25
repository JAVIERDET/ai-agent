"""
utils.py
"""

from pathlib import Path


def _check_suffix(
        item: Path,
        suffix: str
    ) -> str | None:
    """
    Check wheter the path ends with the required suffix
    Params:
        - item: Path to be checked.
        - suffix: String specifying the suffix
        
    Return:
        None if the path ends with the expected suffix. Error string otherwise
    """

    # Check it is a file
    err = _check_is_file(item)
    if err:
        return err

    # Check the suffix:
    if item.suffix != suffix:
        return f'Error: "{item}" is not a Python file.'

    return None


def _check_is_dir(
        item:Path
        ) -> str | None:
    """
    Check wheter the item is a directory. If it isn't return a string error,
    None otherwise
    """
    if not item.is_dir():
        return f'Error: "{item.name}" is not a directory'

    return None


def _check_is_file(
        item:Path
        ) -> str | None:
    """
    Check wheter the item is a file. If it isn't return a string error,
    None otherwise
    """
    if not item.is_file():
        return f'Error: File not found or is not a regular file: "{item}"'

    return None


def _check_is_within_the_scope(
        item: str,
        w_dir:str,
        option:str = "read"
        ) -> str | None:
    """
    Check wheter the item is within the given directory. If it's not return a
    string error, None otherwise.
    Params:
        - item: the path to be checked.
        - w_dir: The path within the item must be located.
        - option (optional): String that indicates the type of operation to be
        performed so information can be added into the error if raised.
    """
    
    # Tranform into Path objects
    item_path: Path = Path(item)
    w_dir_path: Path = Path(w_dir)

    # Join
    full_path = _create_abs_path(w_dir, item_path)
    
    # Check
    if not full_path.is_relative_to(w_dir_path.absolute().resolve()):
        return f'Error: Cannot {option} "{item}" as it is outside the permitted working directory'

    return None


def _create_abs_path(
        w_dir: Path,
        item: Path
        ) -> Path:
    """
    Create an absolute path based on the joined w_dir / item paths.
    Join them, make it absolute and finally resolve
    """

    # Join paths
    full_path = w_dir / item

    # Absolute path
    abs_path = full_path.absolute()

    # Resolve the path (to assess for ../ endings)
    final_path = abs_path.resolve()

    return final_path
