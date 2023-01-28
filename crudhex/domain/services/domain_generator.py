from pathlib import Path
from typing import Optional, Dict, Tuple

from crudhex.domain.models import Entity
from .generation_commons import create_class, create_common_class
from crudhex.domain.services.project_config_context import get_project_config
from crudhex.domain.services.domain import (
    model_generator, command_generator, db_port_generator,
    use_case_port_generator, use_case_generator, not_found_exception_generator
)


def create_model_class(entity: Entity, override: bool = False, folder: Optional[Path] = None) -> Tuple[bool, Path]:
    return create_class(model_generator, entity, override=override,
                        folder=folder, default_folder=Path(get_project_config().get_domain_models_path()))


def create_command_class(entity: Entity, entities_map: Dict[str, Entity],
                         override: bool = False, folder: Optional[Path] = None) -> Tuple[bool, Path]:
    return create_class(command_generator, entity, entities_map,
                        override=override, folder=folder, default_folder=Path(get_project_config().get_domain_commands_path()))


def create_db_port_class(entity: Entity, override: bool = False,
                         folder: Optional[Path] = None) -> Tuple[bool, Path]:
    return create_class(db_port_generator, entity, override=override,
                        folder=folder, default_folder=Path(get_project_config().get_domain_out_ports_path()))


def create_use_case_port_class(entity: Entity, override: bool = False,
                               folder: Optional[Path] = None) -> Tuple[bool, Path]:
    return create_class(use_case_port_generator, entity, override=override,
                        folder=folder, default_folder=Path(get_project_config().get_domain_in_ports_path()))


def create_use_case_class(entity: Entity, override: bool = False,
                          folder: Optional[Path] = None) -> Tuple[bool, Path]:
    return create_class(use_case_generator, entity, override=override,
                        folder=folder, default_folder=Path(get_project_config().get_domain_use_cases_path()))


def create_not_found_exception_class(override: bool = False, folder: Optional[Path] = None) -> Tuple[bool, Path]:
    return create_common_class(not_found_exception_generator, override=override,
                               folder=folder, default_folder=Path(get_project_config().get_domain_exceptions_path()))