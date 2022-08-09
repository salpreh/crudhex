from pathlib import Path
from typing import List

from crudhex.domain.models import Entity
from crudhex.domain.utils.class_type_utils import get_field_imports, get_import
from ..config_context import get_config
from . import command_generator
from . import model_generator

from crudhex.domain.ports import domain_code_writer

_PORT_PREFIX = 'UseCasePort'


def create_port_class(entity: Entity, folder: Path) -> Path:
    if not folder.is_dir(): raise RuntimeError('Output path must be a folder ({})'.format(folder.resolve()))

    class_type = get_port_type_name(entity)
    port_file = folder / f'{class_type}.java'

    id_type = entity.get_id_field().type.class_type
    model_type = model_generator.get_model_type_name(entity)
    command_type = command_generator.get_command_type_name(entity)

    domain_code_writer.create_use_case_port(port_file, class_type, get_package(),
                                            _get_port_imports(entity), id_type, model_type,
                                            command_type, command_type)

    return port_file


def get_package() -> str:
    return get_config().domain_in_ports_pkg


def get_port_type_name(entity: Entity) -> str:
    return f'{entity.name}{_PORT_PREFIX}'


def _get_port_imports(entity: Entity) -> List[str]:
    imports = [
        get_import(command_generator.get_package(), command_generator.get_command_type_name(entity)),
        get_import(model_generator.get_package(), model_generator.get_model_type_name(entity))
    ]
    imports += get_field_imports(entity.get_id_field())

    return imports
