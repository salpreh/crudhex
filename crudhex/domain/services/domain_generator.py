from pathlib import Path
from typing import Optional, Dict

from crudhex.domain.models import Entity
from crudhex.domain.services.config_context import get_config
from crudhex.domain.services.domain import model_generator, command_generator, db_port_generator, use_case_port_generator, use_case_generator


def create_model_class(entity: Entity, folder: Optional[Path] = None) -> Path:
    if not folder:
        folder = Path(get_config().get_domain_models_path())

    return model_generator.create_model_class(entity, folder)


def create_command_class(entity: Entity, entities_map: Dict[str, Entity], folder: Optional[Path] = None) -> Path:
    if not folder:
        folder = Path(get_config().get_domain_commands_path())

    return command_generator.create_command_class(entity, entities_map, folder)


def create_db_port_class(entity: Entity, folder: Optional[Path] = None) -> Path:
    if not folder:
        folder = Path(get_config().get_domain_out_ports_path())

    return db_port_generator.create_port_class(entity, folder)


def create_use_case_port_class(entity: Entity, folder: Optional[Path] = None) -> Path:
    if not folder:
        folder = Path(get_config().get_domain_in_ports_path())

    return use_case_port_generator.create_port_class(entity, folder)


def create_use_case_class(entity: Entity, folder: Optional[Path] = None) -> Path:
    if not folder:
        folder = Path(get_config().get_domain_use_cases_path())

    return use_case_generator.create_use_case_class(entity, folder)
