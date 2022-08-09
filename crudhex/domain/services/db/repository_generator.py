from pathlib import Path
from typing import List, Optional

from crudhex.domain.models import Entity
from crudhex.domain.utils import package_utils
from ..config_context import get_config
from ..type_resolver import get_type_resolver
from . import entity_generator as entity_generator

from crudhex.domain.ports import db_code_writer

DB_REPO_SUFFIX = 'Repository'


def create_repository_class(entity: Entity, folder: Optional[Path] = None) -> Path:
    if not folder.is_dir(): raise RuntimeError('Output path must be a folder ({})'.format(folder.resolve()))

    class_type = get_repository_type_name(entity)
    repo_file = folder / f'{class_type}.java'

    db_code_writer.create_entity_repository(
        repo_file, class_type, get_package(), _get_imports(entity),
        entity_generator.get_entity_type_name(entity), entity.get_id_field().type.class_type
    )

    return repo_file


def get_repository_type_name(entity: Entity) -> str:
    return f'{entity.name}{DB_REPO_SUFFIX}'


def get_package() -> str:
    return get_config().db_repositories_pkg


def _get_imports(entity: Entity) -> List[str]:
    type_resolver = get_type_resolver()

    class_types = [
        package_utils.full_class_name(entity_generator.get_package(), entity_generator.get_entity_type_name(entity))
    ]
    class_types.extend(type_resolver.get_field_types_full_class(entity.get_id_field()))

    return [package_utils.generate_import(ct) for ct in class_types]

