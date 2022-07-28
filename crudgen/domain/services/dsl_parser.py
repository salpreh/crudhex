from typing import Optional, Set, Union, List

from crudgen.domain.config.SpecConfig import SpecConfig
from crudgen.domain.models import IdMeta, Relation, GenerationType, RelationType
from crudgen.domain.models import Entity, Field
from crudgen.domain.services import TypeResolver


def parse_spec_data(spec_data: dict, type_resolver: Optional[TypeResolver] = None) -> List[Entity]:
    entities = []
    # noinspection PyTypeChecker
    generated_types = spec_data.keys()  # type: set
    for name, spec in spec_data.items():
        entities.append(parse_entity_data(name, spec, generated_types, type_resolver))

    return entities


def parse_entity_data(name: str, data: dict, generated_types: Set[str],
                      type_resolver: Optional[TypeResolver]) -> Entity:
    entity = Entity(name)
    entity.meta = parse_entity_meta(data)

    fields_data = data.copy()
    if SpecConfig.META in fields_data: fields_data.pop(SpecConfig.META)

    for name, field_data in fields_data.items():
        entity.fields.append(parse_field(name, field_data, generated_types, type_resolver))

    return entity


def parse_entity_meta(data: dict) -> Optional[Entity.Meta]:
    meta = data.get(SpecConfig.META)
    if not meta or SpecConfig.TABLE not in meta: return None

    return Entity.Meta(meta[SpecConfig.TABLE])


def parse_field(name: str, data: Union[str, dict], generated_types: Set[str],
                type_resolver: Optional[TypeResolver]) -> Field:
    if type(data) is str:
        class_type = data if not type_resolver else type_resolver.resolve_type(data)
        return Field(name, class_type, class_type in generated_types)

    if SpecConfig.TYPE not in data: raise RuntimeError(f'Missing required key {SpecConfig.TYPE}')

    class_type = (data[SpecConfig.TYPE]
                  if not type_resolver
                  else type_resolver.resolve_type(data[SpecConfig.TYPE]))

    field = Field(name, class_type, class_type in generated_types)
    field.column = data.get(SpecConfig.COLUMN)
    field.id_meta = parse_field_id_meta(data)
    field.relation = parse_field_relation(data)

    return field


def parse_field_id_meta(data: dict) -> Optional[IdMeta]:
    id_data = data.get(SpecConfig.ID)
    if not id_data: return None

    if type(id_data) is str:
        return IdMeta(GenerationType(id_data))

    id_meta = IdMeta(GenerationType(id_data[SpecConfig.TYPE]))
    id_meta.sequence = id_data.get(SpecConfig.SEQUENCE)


def parse_field_relation(data: dict) -> Optional[Relation]:
    relation_data = data.get(SpecConfig.RELATION)
    if not relation_data: return None

    relation = Relation(RelationType(relation_data[SpecConfig.TYPE]))
    relation.join_table = relation_data.get(SpecConfig.JOIN_TABLE)
    relation.join_column = relation_data.get(SpecConfig.JOIN_COLUMN)
    relation.inverse_join_column = relation_data.get(SpecConfig.INVERSE_JOIN_COLUMN)

    return relation
