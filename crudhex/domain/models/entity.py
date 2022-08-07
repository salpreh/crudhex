from .field import Field
from typing import List, Optional


class Entity:
    name: str
    meta: Optional['Entity.Meta'] = None
    fields: List[Field]

    def __init__(self, name: str):
        self.name = name
        self.fields = []

    def has_meta(self):
        return self.meta is not None

    def get_id_field(self) -> Optional[Field]:
        for field in self.fields:
            if field.is_id(): return field

        return None

    class Meta:
        table_name: str

        def __init__(self, table_name: str):
            self.table_name = table_name

        def to_dict(self):
            return self.__dict__

        @classmethod
        def default(cls, entity_name: str) -> 'Entity.Meta':
            return cls(entity_name.lower())
