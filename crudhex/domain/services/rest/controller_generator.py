from pathlib import Path
from typing import List, Optional

from crudhex.domain.models import Entity
from crudhex.domain.utils.class_type_utils import get_import, get_field_imports
from crudhex.domain.utils.file_utils import get_java_filename
from ..project_config_context import get_project_config
from ..domain import model_generator as domain_model_generator, command_generator, use_case_port_generator
from . import mapper_generator, model_generator

from crudhex.domain.ports import rest_code_writer
from ...models.field import ClassType
from ...utils.package_utils import full_class_name

_CONTROLLER_SUFFIX = 'Controller'


def create_class(entity: Entity, with_mapper: bool, with_api_page: bool, folder: Optional[Path] = None) -> Path:
    if not folder.is_dir(): raise RuntimeError('Output path must be a folder ({})'.format(folder.resolve()))

    class_type = get_type_name(entity)
    controller_file = folder / get_java_filename(class_type)

    model_type = _get_model_type(entity, with_mapper)
    id_type = entity.get_id_field().type.class_type
    command_type = command_generator.get_type_name(entity)

    use_case_type = use_case_port_generator.get_type_name(entity)
    mapper_type = _get_mapper_type().class_type if with_mapper else None

    rest_code_writer.create_controller(
        controller_file, class_type, get_package(),
        _get_imports(entity, with_mapper), entity.name, model_type,
        id_type, use_case_type, mapper_type,
        command_type, command_type, with_api_page
    )

    return controller_file


def get_type_name(entity: Entity) -> str:
    return f'{entity.name}{_CONTROLLER_SUFFIX}'


def get_package() -> str:
    return get_project_config().rest_controllers_pkg


def get_filename(entity: Entity) -> str:
    return get_java_filename(get_type_name(entity))


def _get_imports(entity: Entity, with_mapping: bool) -> List[str]:
    imports = [
        get_import(command_generator.get_package(), command_generator.get_type_name(entity)),
        get_import(use_case_port_generator.get_package(), use_case_port_generator.get_type_name(entity))
    ]
    imports += get_field_imports(entity.get_id_field())

    if with_mapping:
        imports.append(get_import(mapper_generator.get_package(), mapper_generator.get_type_name()))
        imports.append(get_import(model_generator.get_package(), model_generator.get_type_name(entity)))
    else:
        imports.append(get_import(domain_model_generator.get_package(), domain_model_generator.get_type_name(entity)))

    return imports


def _get_model_type(entity: Entity, with_mapping: bool) -> str:
    if with_mapping:
        return model_generator.get_type_name(entity)

    return domain_model_generator.get_type_name(entity)


def _get_mapper_type() -> ClassType:
    return ClassType(full_class_name(mapper_generator.get_package(), mapper_generator.get_type_name()))
