from collections import namedtuple
from typing import List

from crudhex.domain.models import Field
from crudhex.domain.services.type_resolver import get_type_resolver
from crudhex.domain.utils.package_utils import generate_import


def get_field_imports(field: Field) -> List[str]:
    type_resolver = get_type_resolver()
    if field.type.is_native() or field.type.is_generated: return []

    class_types = type_resolver.get_field_types_full_class(field)

    return [generate_import(ct) for ct in class_types]


def get_field_types(field: Field) -> 'FieldTypes':

    collection_type = None
    collection_type_impl = None
    if field.type.is_collection():
        type_resolver = get_type_resolver()
        collection_type = field.type.collection_type
        collection_type_impl = type_resolver.get_collection_type_impl(field.type.collection_type)

    return FieldTypes(field.type.class_type, collection_type, collection_type_impl)


FieldTypes = namedtuple('FieldTypes', 'class_type collection_type collection_type_impl')
