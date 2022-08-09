from pathlib import Path
from typing import List

from crudhex.domain.models import Entity
from crudhex.domain.utils.class_type_utils import get_field_imports, get_import
from ..config_context import get_config
from . import command_generator
from . import model_generator
from . import use_case_port_generator
from . import db_port_generator

from crudhex.adapters.infrastructure.template_writer import domain_code_writer


_PORT_PREFIX = 'UseCase'


def create_use_case_class(entity: Entity, folder: Path) -> Path:
    if not folder.is_dir(): raise RuntimeError('Output path must be a folder ({})'.format(folder.resolve()))

    class_type = get_use_case_type_name(entity)
    port_file = folder / f'{class_type}.java'

    id_type = entity.get_id_field().type.class_type
    model_type = model_generator.get_model_type_name(entity)
    command_type = command_generator.get_command_type_name(entity)
    db_port = db_port_generator.get_port_type_name(entity)

    domain_code_writer.create_use_case(port_file, class_type, get_package(),
                                       _get_use_case_imports(entity), id_type, model_type,
                                       command_type, command_type, db_port)

    return port_file


def get_package() -> str:
    return get_config().domain_use_cases_pkg


def get_use_case_type_name(entity: Entity) -> str:
    return f'{entity.name}{_PORT_PREFIX}'


def _get_use_case_imports(entity: Entity) -> List[str]:
    imports = use_case_port_generator._get_port_imports(entity)
    imports.extend([
        get_import(use_case_port_generator.get_package(), use_case_port_generator.get_port_type_name(entity)),
        get_import(db_port_generator.get_package(), db_port_generator.get_port_type_name(entity))

    ])

    return imports

