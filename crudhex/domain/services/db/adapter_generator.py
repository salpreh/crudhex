from pathlib import Path
from typing import List, Dict

from crudhex.domain.models import Entity, Field
from crudhex.domain.utils.class_type_utils import get_import, get_type_import, get_resolved_import
from . import entity_generator, repository_generator
from ..config_context import get_config
from ..domain import command_generator, model_generator, db_port_generator
from ...models.RelationData import RelationData
from ...models.field import ClassType
from crudhex.domain.ports import db_code_writer

_ADAPTER_PREFIX = 'DatasourceAdapter'
_DEFAULT_MAPPER_TYPE = 'Mapper'


def create_adapter_class(entity: Entity, entities_map: Dict[str, Entity], folder: Path) -> Path:
    if not folder.is_dir(): raise RuntimeError('Output path must be a folder ({})'.format(folder.resolve()))

    class_type = get_adapter_type_name(entity)
    adapter_file = folder / f'{class_type}.java'

    model_type = model_generator.get_model_type_name(entity)
    entity_type = entity_generator.get_entity_type_name(entity)
    id_type = entity.get_id_field().type.class_type
    command_type = command_generator.get_command_type_name(entity)
    repository_type = repository_generator.get_repository_type_name(entity)
    db_port = db_port_generator.get_port_type_name(entity)
    relations_data = [d.to_dict() for d in _get_relations_data(entity, entities_map)]

    db_code_writer.create_adapter(adapter_file, class_type, get_package(), db_port,
                                  _get_adapter_imports(entity, entities_map), model_type, entity_type, id_type,
                                  repository_type, command_type, command_type,
                                  relations_data, _get_mapper_type().class_type)

    return adapter_file


def get_package() -> str:
    return get_config().domain_use_cases_pkg


def get_adapter_type_name(entity: Entity) -> str:
    return f'{entity.name}{_ADAPTER_PREFIX}'


def _get_mapper_type() -> ClassType:
    config_mapper = get_config().db_mapper_class
    if not config_mapper:
        return ClassType(_DEFAULT_MAPPER_TYPE, True)

    return ClassType(config_mapper)


def _get_adapter_imports(entity: Entity, entities_map: Dict[str, Entity]) -> List[str]:
    imports = set(db_port_generator._get_port_imports(entity))
    imports.update([
        get_import(entity_generator.get_package(), entity_generator.get_entity_type_name(entity)),
        get_import(repository_generator.get_package(), repository_generator.get_repository_type_name(entity)),
        get_import(db_port_generator.get_package(), db_port_generator.get_port_type_name(entity))

    ])

    mapper_type = _get_mapper_type()
    if not mapper_type.is_generated:
        imports.add(get_type_import(mapper_type))

    # Getting updated relations classes (entity and repository)
    for field in _get_command_relation_fields(entity):
        related_entity = entities_map.get(field.type.class_type)
        if not related_entity: continue

        imports.update([
            get_import(entity_generator.get_package(), entity_generator.get_entity_type_name(related_entity)),
            get_import(repository_generator.get_package(), repository_generator.get_repository_type_name(related_entity))
        ])
        if field.type.collection_type:
            imports.add(get_resolved_import(field.type.collection_type))

    return list(imports)


def _get_relations_data(entity: Entity, entities_map: Dict[str, Entity]) -> List[RelationData]:
    relations_data = []
    for field in _get_command_relation_fields(entity):
        related_entity = entities_map.get(field.type.class_type, Entity(field.type.class_type))

        relation_data = RelationData(field.name)
        relation_data.collection_type = field.type.collection_type
        relation_data.entity_type = entity_generator.get_entity_type_name(related_entity)
        relation_data.repository_type = repository_generator.get_repository_type_name(related_entity)
        relation_data.create_command_type = command_generator.get_command_type_name(related_entity)
        relation_data.update_command_type = command_generator.get_command_type_name(related_entity)

        relations_data.append(relation_data)

    return relations_data


def _get_command_relation_fields(entity: Entity) -> List[Field]:
    return [f for f in command_generator.get_command_used_fields(entity) if f.has_relation()]
