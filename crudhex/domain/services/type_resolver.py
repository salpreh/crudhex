from typing import Dict, Optional, List

from crudhex.domain.models import Field
from crudhex.domain.utils import package_utils

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

    _TYPE_DATA = {
        # Java
        'Collection': 'java.util.Collection',
        'List': 'java.util.List',
        'ArrayList': 'java.util.ArrayList',
        'Set': 'java.util.Set',
        'HashSet': 'java.util.HashSet',
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
        # Spring data
        'Page': 'org.springframework.data.domain.Page',
        'Pageable': 'org.springframework.data.domain.Pageable',

    }

    _COLLECTION_INTERFACES = [
        'Collection',
        'List',
        'Map',
        'Set'
    ]

    _COLLECTION_IMPL = {
        'Collection': 'ArrayList',
        'List': 'ArrayList',
        'Set': 'HashSet',
        'Map': 'HashMap'
    }

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

    def get_field_types_full_class(self, field: Field, filter_native: bool = False, filter_generated: bool = True) -> List[str]:
        if filter_native and field.type.is_native(): return []

        field_types = []
        if not field.type.is_generated or not filter_generated:
            class_type = field.type.get_full_class_type()
            field_types.append(self.resolve_type(class_type))

        if not field.type.is_collection():
            return field_types

        field_types.append(self.resolve_type(field.type.collection_type))
        if self._is_collection_interface(field.type.collection_type):
            impl_type = self._get_collection_default_impl(field.type.collection_type)
            field_types.append(self.resolve_type(impl_type))

        return field_types

    def get_collection_type_impl(self, class_type: str) -> str:
        class_name = package_utils.get_class_name(class_type)

        # If not found in implementation map we assume is a collection implementation. Return same class then.
        if not self._is_collection_interface(class_name): return class_name

        return self._get_collection_default_impl(class_name)

    def _init(self):
        self.type_data.update(**TypeResolver._TYPE_DATA)

    def _is_collection_interface(self, class_type: str) -> bool:
        return class_type in TypeResolver._COLLECTION_INTERFACES

    def _get_collection_default_impl(self, class_type: str) -> str:
        return TypeResolver._COLLECTION_IMPL[class_type]
