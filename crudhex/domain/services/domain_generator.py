from pathlib import Path
from typing import Optional, Dict, Tuple

from crudhex.domain.models import Entity
from ..utils.file_utils import create_first_folder
from crudhex.domain.services.config_context import get_config
from crudhex.domain.services.domain import (
    model_generator, command_generator, db_port_generator,
    use_case_port_generator, use_case_generator
)


def create_model_class(entity: Entity, override: bool = False, folder: Optional[Path] = None) -> Tuple[bool, Path]:
    folder = create_first_folder(folder, Path(get_config().get_domain_models_path()))
    file = folder / model_generator.get_filename(entity)
    if not override and file.exists():
        return False, file

    return True, model_generator.create_class(entity, folder)


def create_command_class(entity: Entity, entities_map: Dict[str, Entity],
                         override: bool = False, folder: Optional[Path] = None) -> Tuple[bool, Path]:
    folder = create_first_folder(folder, Path(get_config().get_domain_commands_path()))
    file = folder / command_generator.get_filename(entity)
    if not override and file.exists():
        return False, file

    return True, command_generator.create_class(entity, entities_map, folder)


def create_db_port_class(entity: Entity, override: bool = False,
                         folder: Optional[Path] = None) -> Tuple[bool, Path]:
    folder = create_first_folder(folder, Path(get_config().get_domain_out_ports_path()))
    file = folder / db_port_generator.get_filename(entity)
    if not override and file.exists():
        return False, file

    return True, db_port_generator.create_class(entity, folder)


def create_use_case_port_class(entity: Entity, override: bool = False,
                               folder: Optional[Path] = None) -> Tuple[bool, Path]:
    folder = create_first_folder(folder, Path(get_config().get_domain_in_ports_path()))
    file = folder / use_case_port_generator.get_filename(entity)
    if not override and file.exists():
        return False, file

    return True, use_case_port_generator.create_class(entity, folder)


def create_use_case_class(entity: Entity, override: bool = False,
                          folder: Optional[Path] = None) -> Tuple[bool, Path]:
    folder = create_first_folder(folder, Path(get_config().get_domain_use_cases_path()))
    file = folder / use_case_generator.get_filename(entity)
    if not override and file.exists():
        return False, file

    return True, use_case_generator.create_class(entity, folder)
