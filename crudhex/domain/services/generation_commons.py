from pathlib import Path
from typing import Optional, Tuple, Union, Any, Dict
from typing_extensions import Protocol

from crudhex.domain.models import Entity
from crudhex.domain.utils.file_utils import create_first_folder


def create_class(generator: Union['IGenerator', Any], entity: Entity, *args,
                 override: bool = False, folder: Optional[Path] = None, default_folder: Path) -> Tuple[bool, Path]:

    folder = create_first_folder(folder, default_folder)
    file = folder / generator.get_filename(entity)
    if not override and file.exists():
        return False, file

    return True, generator.create_class(entity, *args, folder)


def create_shared_class(generator: Union['ISharedGenerator', Any], entities_map: [str, Entity], *args,
                        override: bool = False, folder: Optional[Path] = None, default_folder: Path) -> Tuple[bool, Path]:

    folder = create_first_folder(folder, default_folder)
    file = folder / generator.get_filename()
    if not override and file.exists():
        return False, file

    return True, generator.create_class(entities_map, *args, folder)


def create_common_class(generator: Union['ICommonGenerator', Any], *args,
                        override: bool = False, folder: Optional[Path] = None, default_folder: Path) -> Tuple[bool, Path]:

    folder = create_first_folder(folder, default_folder)
    file = folder / generator.get_filename()
    if not override and file.exists():
        return False, file

    return True, generator.create_class(*args, folder)


class IGenerator(Protocol):

    @staticmethod
    def create_class(entity: Entity, *args) -> Path:
        ...

    @staticmethod
    def get_package(self) -> str:
        ...

    @staticmethod
    def get_type_name(entity: Entity) -> str:
        ...

    @staticmethod
    def get_filename(entity: Entity) -> str:
        ...


class ISharedGenerator(Protocol):

    @staticmethod
    def create_class(entities_map: Dict[str, Entity], *args) -> Path:
        ...

    @staticmethod
    def get_package() -> str:
        ...

    @staticmethod
    def get_type_name() -> str:
        ...

    @staticmethod
    def get_filename() -> str:
        ...


class ICommonGenerator(Protocol):
    @staticmethod
    def create_class(*args) -> Path:
        ...

    @staticmethod
    def get_package() -> str:
        ...

    @staticmethod
    def get_type_name() -> str:
        ...

    @staticmethod
    def get_filename() -> str:
        ...