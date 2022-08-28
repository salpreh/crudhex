"""
Implements `ISharedClass` protocol interface
"""
from pathlib import Path
from typing import List, Dict

from crudhex.domain.models import Entity
from crudhex.domain.utils.class_type_utils import get_import, get_type_import, get_resolved_import
from crudhex.domain.utils import package_utils
from crudhex.domain.utils.file_utils import get_java_filename
from . import entity_generator
from ..config_context import get_config
from ..domain import model_generator
from crudhex.domain.ports import db_code_writer
from ...models.mapper import MapperType

_MAPPER_NAME = 'DbMapper'


def create_class(entities_map: Dict[str, Entity], mapper_type: MapperType, folder: Path) -> Path:
    if not folder.is_dir(): raise RuntimeError('Output path must be a folder ({})'.format(folder.resolve()))

    class_type = get_type_name()
    mapper_file = folder / get_java_filename(class_type)
    mappings = {entity_generator.get_type_name(e): model_generator.get_type_name(e) for e in entities_map.values()}

    db_code_writer.create_mapper(mapper_file, class_type, get_package(),
                                 _get_imports(entities_map), mappings, mapper_type)

    return mapper_file


def get_package() -> str:
    config = get_config()
    if config.db_mapper_class: return package_utils.get_package(config.db_mapper_class)

    return get_config().db_mapper_pkg


def get_type_name() -> str:
    config = get_config()
    if config.db_mapper_class: return package_utils.get_class_name(config.db_mapper_class)

    return _MAPPER_NAME


def get_filename() -> str:
    return get_java_filename(get_type_name())


def _get_imports(entities_map: Dict[str, Entity]) -> List[str]:
    imports = []
    for entity in entities_map.values():
        imports.extend([
            get_import(entity_generator.get_package(), entity_generator.get_type_name(entity)),
            get_import(model_generator.get_package(), model_generator.get_type_name(entity))
        ])

    return imports
