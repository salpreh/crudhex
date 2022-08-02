from typing import Dict, Optional, List

from crudgen.domain.models import Field

_TYPE_RESOLVER: Optional['TypeResolver'] = None


def get_type_resolver(additional_types: Dict[str, str] = None) -> 'TypeResolver':
    global _TYPE_RESOLVER
    if not _TYPE_RESOLVER:
        _TYPE_RESOLVER = TypeResolver()

    if additional_types: _TYPE_RESOLVER.add_additional_types(additional_types)

    return _TYPE_RESOLVER


class TypeResolver:
    DEFAULT_COLLECTION = 'Set'
    DEFAULT_COLLECTION_IMPL = 'HashSet'
    GENERIC_TEMPLATE = '{}<{}>'

    type_data: Dict[str, str]

    def __init__(self, additional_types: Dict[str, str] = None):
        self.type_data = {}
        self._init()

        if additional_types:
            self.type_data.update(**additional_types)

    def resolve_type(self, class_type: str):
        return self.type_data.get(class_type, class_type)

    def add_additional_types(self, types: Dict[str, str]):
        self.type_data.update(**types)

    def get_field_types_full_class(self, field: Field, filter_native: bool = False) -> List[str]:
        if filter_native and field.type.is_native(): return []

        field_types = []
        if field.has_relation() and field.relation.type.has_multiple():
            field_types.append(self.resolve_type(TypeResolver.DEFAULT_COLLECTION))
            field_types.append(self.resolve_type(TypeResolver.DEFAULT_COLLECTION_IMPL))

        field_types.append(field.type.get_qualified_class_type())

        return field_types

    def _init(self):
        type_data = {
            'Collection': 'java.util.Collection',
            'List': 'java.util.List',
            'ArrayList': 'java.util.ArrayList',
            'Set': 'java.util.Set',
            'Map': 'java.util.Map',
            'HashMap': 'java.util.HashMap',
            'UUID': 'java.util.UUID',
            'Optional': 'java.util.Optional',
            'Stream': 'java.util.stream.Stream',
            'String': 'java.lang.String',
            'Double': 'java.lang.Double',
            'Float': 'java.lang.Float',
            'Integer': 'java.lang.Integer',
            'Short': 'java.lang.Short',
            'Long': 'java.lang.Long',
            'Boolean': 'java.lang.Boolean',
            'BigDecimal': 'java.math.BigDecimal',
            'BigInteger': 'java.math.BigInteger',
        }

        self.type_data.update(**type_data)