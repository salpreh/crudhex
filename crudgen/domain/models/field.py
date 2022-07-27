from enum import Enum
from typing import Optional

from crudgen.domain.utils.package_utils import parse_class_name, full_class_name


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

    def is_id(self):
        return self.id_meta is not None

    def is_relation(self):
        return self.relation is not None


class Relation:
    type: 'RelationType'
    join_table: Optional[str]
    join_column: Optional[str]
    inverse_join_column: Optional[str]

    def __init__(self, type: 'RelationType'):
        self.type = type
        self.join_table = None
        self.join_column = None
        self.inverse_join_column = None

    class RelationType(Enum):
        ONE_TO_ONE = 'one-to-one'
        ONE_TO_MANY = 'one-to-many'
        MANY_TO_ONE = 'many-to-one'
        MANY_TO_MANY = 'many-to-many'


class IdMeta:
    type: 'GenerationType'
    sequence: str

    def __init__(self, type: 'GenerationType'):
        self.type = type
        self.sequence = None

    class GenerationType(Enum):
        NONE = 'none'
        SEQUENCE = 'sequence'
        IDENTITY = 'identity'
        AUTO = 'auto'


class ClassType:
    package: Optional[str]
    class_type: str
    is_generated: bool

    def __init__(self, class_name: str, is_generated: bool = False):
        class_data = parse_class_name(class_name)
        self.package = class_data[0]
        self.class_type = class_data[1]
        self.is_generated = is_generated

    def get_qualifyed_class_type(self):
        return full_class_name(self.package, self.class_type)