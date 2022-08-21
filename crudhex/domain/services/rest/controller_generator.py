from pathlib import Path
from typing import List, Optional

from crudhex.domain.models import Entity
from crudhex.domain.utils.class_type_utils import get_import, get_field_imports
from crudhex.domain.utils.file_utils import get_java_filename
from ..config_context import get_config
from ..domain import model_generator, command_generator, use_case_port_generator

from crudhex.domain.ports import rest_code_writer

_CONTROLLER_SUFFIX = 'Controller'


def create_controller_class(entity: Entity, folder: Optional[Path] = None) -> Path:
    if not folder.is_dir(): raise RuntimeError('Output path must be a folder ({})'.format(folder.resolve()))

    class_type = get_controller_type_name(entity)
    controller_file = folder / get_java_filename(class_type)

    model_type = model_generator.get_type_name(entity)
    id_type = entity.get_id_field().type.class_type
    use_case_type = use_case_port_generator.get_type_name(entity)
    command_type = command_generator.get_type_name(entity)

    rest_code_writer.create_controller(
        controller_file, class_type, get_package(), _get_imports(entity),
        entity.name, model_type, id_type,
        use_case_type, command_type, command_type
    )

    return controller_file


def get_controller_type_name(entity: Entity) -> str:
    return f'{entity.name}{_CONTROLLER_SUFFIX}'


def get_package() -> str:
    return get_config().rest_controllers_pkg


def get_filename(entity: Entity) -> str:
    return get_java_filename(get_controller_type_name(entity))


def _get_imports(entity: Entity) -> List[str]:
    imports = [
        get_import(model_generator.get_package(), model_generator.get_type_name(entity)),
        get_import(command_generator.get_package(), command_generator.get_type_name(entity)),
        get_import(use_case_port_generator.get_package(), use_case_port_generator.get_type_name(entity))
    ]
    imports += get_field_imports(entity.get_id_field())

    return imports

