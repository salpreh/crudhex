from typing import Optional

from crudhex.domain.models import Field, GenerationType, RelationType
from tests.utils.file_utils import load_fixture_file
from crudhex.domain.services.dsl_parser import parse_spec_data


SINGLE_TYPE = 'single_type.yaml'
ID_SPEC_TYPE = 'id_full_spec.yaml'
WITH_RELATIONS_TYPE = 'with_relations_type.yaml'
MULTIPLE_TYPES = 'multi_types.yaml'


def test_single_type_parse():
    # given
    spec_data = load_fixture_file(SINGLE_TYPE)

    # when
    entities = parse_spec_data(spec_data)

    # then
    assert len(entities) == 1

    entity = entities[0]
    assert entity.name == 'Person'
    assert entity.meta.table_name == 'persons'
    assert len(entity.fields) == 4

    _assert_field(entity.fields[0], 'id', 'Long')
    _assert_id_field(entity.fields[0], GenerationType.SEQUENCE)

    _assert_field(entity.fields[1], 'name', 'String')
    _assert_field(entity.fields[2], 'age', 'int')
    _assert_field(entity.fields[3], 'race', 'com.salpreh.baseapi.domain.models.RaceType')


def test_id_full_spec_type_parse():
    # given
    spec_data = load_fixture_file(ID_SPEC_TYPE)

    # when
    entities = parse_spec_data(spec_data)

    # then
    assert len(entities) == 1

    entity = entities[0]
    assert entity.name == 'Person'
    assert len(entity.fields) == 4

    _assert_field(entity.fields[0], 'id', 'Long')
    _assert_id_field(entity.fields[0], GenerationType.SEQUENCE, 'person_pk_seq')


def test_with_relation_type_parse():
    # given
    spec_data = load_fixture_file(WITH_RELATIONS_TYPE)

    # when
    entities = parse_spec_data(spec_data)

    # then
    assert len(entities) == 1

    entity = entities[0]
    assert entity.name == 'Person'

    fields = entity.fields
    _assert_field(fields[1], 'birthPlanet', 'Planet')
    _assert_field_relation_m21(fields[1], 'birth_planet_id')

    _assert_field(fields[2], 'affiliations', 'Faction')
    _assert_field_relation_m2m(fields[2], 'person_id', 'faction_id', 'person_affiliation')

    _assert_field(fields[3], 'backup', 'Person')
    _assert_field_relation_121(fields[3])

    _assert_field(fields[4], 'backing', 'Person')
    _assert_field_relation_121(fields[4], None, 'backup')


def test_multi_types_parse():
    # given
    spec_data = load_fixture_file(MULTIPLE_TYPES)

    # when
    entities = parse_spec_data(spec_data)

    # then
    assert len(entities) == 3

    entity = entities[0]
    assert entity.name == 'Person'
    assert len(entity.fields) == 6
    assert entity.fields[4].type.is_generated
    assert entity.fields[5].type.is_generated

    entity = entities[1]
    assert entity.name == 'Planet'
    assert len(entity.fields) == 4
    assert entity.fields[2].type.is_generated
    assert entity.fields[3].type.is_generated

    entity = entities[2]
    assert entity.name == 'Faction'
    assert len(entity.fields) == 4
    assert entity.fields[2].type.is_generated
    assert entity.fields[3].type.is_generated


def _assert_id_field(field: Field, generation: GenerationType, sequence: Optional[str] = None):
    assert field.id_meta
    assert field.id_meta.generation == generation
    assert field.id_meta.sequence == sequence


def _assert_field(field: Field, name: str, class_type: str):
    assert field.name == name
    assert field.type.get_qualified_class_type() == class_type


def _assert_field_relation_12m(field: Field, join_column: Optional[str] = None):
    assert field.relation
    assert field.relation.type == RelationType.ONE_TO_MANY
    assert field.relation.join_column == join_column


def _assert_field_relation_m21(field: Field, join_column: Optional[str] = None):
    assert field.relation
    assert field.relation.type == RelationType.MANY_TO_ONE
    assert field.relation.join_column == join_column


def _assert_field_relation_m2m(field: Field, join_column: Optional[str] = None,
                               inverse_join_column: Optional[str] = None, join_table: Optional[str] = None):
    assert field.relation
    assert field.relation.type == RelationType.MANY_TO_MANY
    assert field.relation.join_column == join_column
    assert field.relation.inverse_join_column == inverse_join_column
    assert field.relation.join_table == join_table


def _assert_field_relation_121(field: Field, join_column: Optional[str] = None, mapped_by: Optional[str] = None):
    assert field.relation
    assert field.relation.type == RelationType.ONE_TO_ONE
    assert field.relation.join_column == join_column
