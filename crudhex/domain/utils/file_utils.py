from pathlib import Path
from typing import Optional


def create_first_folder(*args: Optional[Path]) -> Path:
    """
    Returns the first non `None` folder. Creates the folder if needed.
    :param args: None or Paths
    :return: First non None path
    :raises RuntimeError If all args are None
    """
    for file in args:
        if file is not None:
            file.mkdir(exist_ok=True, parents=True)
            return file

    raise RuntimeError('All provided paths are None')


def get_java_filename(class_type: str) -> str:
    return f'{class_type}.java'
