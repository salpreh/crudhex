from .field import Field
from typing import List, Optional


class Entity:
    name: str
    meta: Optional['Meta']
    fields: List[Field]

    def __init__(self, name: str):
        self.name = name
        self.fields = []
        self.meta = None

    def has_meta(self):
        return self.meta is not None

    class Meta:
        table_name: str

        def __init__(self, table_name: str):
            self.table_name = table_name
