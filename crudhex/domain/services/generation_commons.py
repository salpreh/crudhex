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


class IGenerator(Protocol):

    def create_class(self, entity: Entity, *args) -> Path:
        ...

    def get_package(self) -> str:
        ...

    def get_type_name(self, entity: Entity) -> str:
        ...

    def get_filename(self, entity: Entity) -> str:
        ...


class ISharedGenerator(Protocol):

    def create_class(self, entities_map: Dict[str, Entity], *args) -> Path:
        ...

    def get_package(self) -> str:
        ...

    def get_type_name(self) -> str:
        ...

    def get_filename(self) -> str:
        ...
