from pathlib import Path
from typing import List, Dict

from crudhex.domain.models import Entity, Field
from crudhex.domain.utils.class_type_utils import get_field_imports, get_field_types
from crudhex.domain.utils.file_utils import get_java_filename
from ..project_config_context import get_project_config

from crudhex.domain.ports import domain_code_writer

_COMMAND_SUFFIX = 'UpsertCommand'


def create_class(entity: Entity, entities_map: Dict[str, Entity], folder: Path) -> Path:
    if not folder.is_dir(): raise RuntimeError('Output path must be a folder ({})'.format(folder.resolve()))

    class_type = get_type_name(entity)
    model_file = folder / get_java_filename(class_type)

    domain_code_writer.create_command(model_file, get_type_name(entity), get_package(),
                                      _get_imports(entity, entities_map), _get_command_fields_data(entity, entities_map))

    return model_file


def get_package() -> str:
    return get_project_config().domain_commands_pkg


def get_type_name(entity: Entity) -> str:
    return f'{entity.name}{_COMMAND_SUFFIX}'


def get_filename(entity: Entity) -> str:
    return get_java_filename(get_type_name(entity))


def get_used_fields(entity: Entity) -> List[Field]:
    return [f for f in entity.fields if _is_used_field(f)]


def _get_imports(entity: Entity, entities_map: Dict[str, Entity]) -> List[str]:
    imports = set()
    for field in entity.fields:
        if not _is_used_field(field): continue
        if field.has_relation():
            related_entity = entities_map.get(field.type.class_type)
            field = _get_relation_id_field_data(related_entity, field)

        imports.update(set(get_field_imports(field)))

    return list(imports)


def _get_command_fields_data(entity: Entity, entities_map: Dict[str, Entity]) -> List[Dict[str, str]]:
    fields_data = []
    for field in entity.fields:
        # Exclude non owning relation side getters to avoid loops in serialization
        if not _is_used_field(field): continue
        fields_data.append(_get_field_data(field, entities_map))

    return fields_data


def _get_field_data(field: Field, entities_map: Dict[str, Entity]) -> Dict[str, str]:
    field_data = {
        'name': field.name
    }
    if field.has_relation():
        related_entity = entities_map.get(field.type.class_type)
        field = _get_relation_id_field_data(related_entity, field)

    field_data.update(get_field_types(field)._asdict())

    return field_data


def _get_relation_id_field_data(entity: Entity, relation_field: Field) -> Field:
    id_field = entity.get_id_field()
    if not id_field: raise RuntimeError('No id field found for entity {}'.format(entity.name))

    id_relation_field = Field(relation_field.name, id_field.type.class_type, False)
    id_relation_field.type.collection_type = relation_field.type.collection_type

    return id_relation_field


def _is_used_field(field: Field) -> bool:
    inverse_relation = field.has_relation() and field.relation.mapped_by
    return not inverse_relation and not field.is_id()
