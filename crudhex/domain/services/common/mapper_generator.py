from pathlib import Path
from typing import List, Dict, NamedTuple

from crudhex.domain.models import Entity
from crudhex.domain.utils.class_type_utils import get_import
from crudhex.domain.utils import package_utils
from crudhex.domain.utils.file_utils import get_java_filename
from ..project_config_context import get_project_config
from crudhex.domain.ports import db_code_writer
from ..generation_commons import IGenerator
from ...models.mapper import MapperType

MapperParams = NamedTuple('MapperParams', [('from_generator', IGenerator), ('to_generator', IGenerator),
                                           ('package', str), ('type_name', str)])


def create_class(entities_map: Dict[str, Entity], mapper_type: MapperType, folder: Path, params: MapperParams) -> Path:
    if not folder.is_dir(): raise RuntimeError('Output path must be a folder ({})'.format(folder.resolve()))

    class_type = params.type_name
    mapper_file = folder / get_java_filename(class_type)
    mappings = {params.from_generator.get_type_name(e): params.to_generator.get_type_name(e) for e in entities_map.values()}

    db_code_writer.create_mapper(mapper_file, class_type, params.package,
                                 _get_imports(entities_map, params.from_generator, params.to_generator),
                                 mappings, mapper_type)

    return mapper_file


def get_package(mapper_class_key: str, mapper_pkg_key: str) -> str:
    config = get_project_config()
    if getattr(config, mapper_class_key): return package_utils.get_package(getattr(config, mapper_class_key))

    return getattr(config, mapper_pkg_key)


def get_type_name(mapper_class_key: str, default_name: str) -> str:
    config = get_project_config()
    if getattr(config, mapper_class_key): return package_utils.get_class_name(getattr(config, mapper_class_key))

    return default_name


def get_filename(mapper_class_key: str, default_name: str) -> str:
    return get_java_filename(get_type_name(mapper_class_key, default_name))


def _get_imports(entities_map: Dict[str, Entity], from_generator: IGenerator, to_generator: IGenerator) -> List[str]:
    imports = []
    for entity in entities_map.values():
        imports.extend([
            get_import(from_generator.get_package(), from_generator.get_type_name(entity)),
            get_import(to_generator.get_package(), to_generator.get_type_name(entity))
        ])

    return imports
