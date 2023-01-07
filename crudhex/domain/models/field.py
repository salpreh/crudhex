from enum import Enum
from typing import Optional
import uuid

from crudhex.domain.utils.package_utils import parse_class_name, full_class_name


class Field:
    name: str
    type: 'ClassType'
    column: Optional[str]
    id_meta: Optional['IdMeta']
    relation: Optional['Relation']

    def __init__(self, name: str, class_type: str, is_generated: bool = False):
        self.name = name
        self.type = ClassType(class_type, is_generated)
        self.column = None
        self.id_meta = None
        self.relation = None

    def is_id(self) -> bool:
        return self.id_meta is not None

    def has_relation(self) -> bool:
        return self.relation is not None

    def get_column_or_default(self) -> str:
        if not self.column: return self.name.lower()

        return self.column


class Relation:
    type: 'RelationType'
    join_table: Optional[str]
    join_column: Optional[str]
    inverse_join_column: Optional[str]
    mapped_by: Optional[str]

    def __init__(self, relation_type: 'RelationType'):
        self.type = relation_type
        self.join_table = None
        self.join_column = None
        self.inverse_join_column = None

    def to_dict(self):
        return self.__dict__


class IdMeta:
    generation: 'GenerationType'
    sequence: Optional[str]

    def __init__(self, generation: 'GenerationType'):
        self.generation = generation
        self.sequence = None

    def get_sequence_or_default(self, id_name: Optional[str] = None) -> str:
        if self.sequence: return self.sequence

        if not id_name:
            id_name = str(uuid.uuid4()).replace('-', '')

        return f'{id_name}_pk_gen'

    def to_dict(self):
        data = self.__dict__
        data['sequence'] = self.get_sequence_or_default()

        return data


class ClassType:
    package: Optional[str]
    class_type: str
    collection_type: Optional[str]
    is_generated: bool

    def __init__(self, class_name: str, is_generated: bool = False):
        class_data = parse_class_name(class_name)
        self.package = class_data[0]
        self.class_type = class_data[1]
        self.collection_type = None
        self.is_generated = is_generated

    def get_full_class_type(self) -> str:
        return full_class_name(self.package, self.class_type)

    def is_native(self) -> bool:
        return self.class_type[0].islower()

    def is_collection(self) -> bool:
        return self.collection_type is not None


class GenerationType(Enum):
    NONE = 'none'
    SEQUENCE = 'sequence'
    IDENTITY = 'identity'
    AUTO = 'auto'


class RelationType(Enum):
    ONE_TO_ONE = 'one-to-one'
    ONE_TO_MANY = 'one-to-many'
    MANY_TO_ONE = 'many-to-one'
    MANY_TO_MANY = 'many-to-many'

    def has_multiple(self) -> bool:
        return self in [RelationType.ONE_TO_MANY, RelationType.MANY_TO_MANY]
