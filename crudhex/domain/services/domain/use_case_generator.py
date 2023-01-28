from pathlib import Path
from typing import List

from crudhex.domain.models import Entity
from crudhex.domain.utils.class_type_utils import get_import
from crudhex.domain.utils.file_utils import get_java_filename
from ..project_config_context import get_project_config
from . import command_generator
from . import model_generator
from . import use_case_port_generator
from . import db_port_generator

from crudhex.domain.ports import domain_code_writer

_USE_CASE_PREFIX = 'UseCase'


def create_class(entity: Entity, folder: Path) -> Path:
    if not folder.is_dir(): raise RuntimeError('Output path must be a folder ({})'.format(folder.resolve()))

    class_type = get_type_name(entity)
    use_case_file = folder / get_java_filename(class_type)

    id_type = entity.get_id_field().type.class_type
    model_type = model_generator.get_type_name(entity)
    command_type = command_generator.get_type_name(entity)
    db_port = db_port_generator.get_type_name(entity)
    class_type_interface = use_case_port_generator.get_type_name(entity)

    domain_code_writer.create_use_case(use_case_file, class_type, get_package(), class_type_interface,
                                       _get_imports(entity), id_type, model_type, command_type,
                                       command_type, db_port)

    return use_case_file


def get_package() -> str:
    return get_project_config().domain_use_cases_pkg


def get_type_name(entity: Entity) -> str:
    return f'{entity.name}{_USE_CASE_PREFIX}'


def get_filename(entity: Entity) -> str:
    return get_java_filename(get_type_name(entity))


def _get_imports(entity: Entity) -> List[str]:
    imports = use_case_port_generator._get_imports(entity)
    imports.extend([
        get_import(use_case_port_generator.get_package(), use_case_port_generator.get_type_name(entity)),
        get_import(db_port_generator.get_package(), db_port_generator.get_type_name(entity))

    ])

    return imports

