from pathlib import Path
from typing import Dict, List

from crudhex.domain.models import Entity, Field
from crudhex.domain.utils.package_utils import generate_import
from ..config_context import get_config
from ..type_resolver import get_type_resolver

from crudhex.adapters.infrastructure.template_writer import db_entity_code_writer

DB_ENTITY_SUFFIX = 'Entity'


def create_entity_class(entity: Entity, folder: Path) -> Path:
    if not folder.is_dir(): raise RuntimeError('Output path must be a folder ({})'.format(folder.resolve()))

    class_type = get_entity_type_name(entity)
    entity_file = folder / f'{class_type}.java'

    db_entity_code_writer.create_entity(
        entity_file, class_type, get_package(),
        _get_entity_imports(entity), _get_entity_meta(entity), _get_entity_fields_data(entity)
    )

    return entity_file


def get_package() -> str:
    return get_config().db_models_pkg


def get_entity_type_name(entity: Entity) -> str:
    return f'{entity.name}{DB_ENTITY_SUFFIX}'


def _get_entity_meta(entity: Entity) -> Dict[str, str]:
    meta = entity.meta
    if not meta:
        meta = Entity.Meta.default(entity.name)

    return meta.to_dict()


def _get_entity_imports(entity: Entity) -> List[str]:
    imports = []
    for field in entity.fields:
        imports += _get_entity_field_imports(field)

    return imports


def _get_entity_field_imports(field: Field) -> List[str]:
    type_resolver = get_type_resolver()
    if field.type.is_native() or field.type.is_generated: return []

    class_types = type_resolver.get_field_types_full_class(field)

    return [generate_import(ct) for ct in class_types]


def _get_entity_fields_data(entity: Entity) -> List[Dict[str, str]]:
    fields_data = []
    for field in entity.fields:
        fields_data.append(_get_field_data(field))

    return fields_data


def _get_field_data(field: Field) -> Dict[str, str]:
    field_data = {
        'class_type': field.type.class_type,
        'name': field.name,
        'column_name': field.column,
        'relationship': False,
        'id': False
    }

    if field.type.is_collection():
        type_resolver = get_type_resolver()
        field_data['collection_type'] = field.type.collection_type
        field_data['collection_type_impl'] = type_resolver.get_collection_type_impl(field.type.collection_type)

    if field.is_id():
        field_data['id'] = True
        field_data.update(**field.id_meta.to_dict())

    elif field.has_relation():
        field_data['relationship'] = field.relation.type
        field_data.update(**field.relation.to_dict())

    return field_data
