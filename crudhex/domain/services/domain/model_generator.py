from pathlib import Path
from typing import List, Dict

from crudhex.domain.models import Entity, Field
from crudhex.domain.utils.class_type_utils import get_field_imports, get_field_types
from ..config_context import get_config

from crudhex.domain.ports import domain_code_writer


def create_model_class(entity: Entity, folder: Path) -> Path:
    if not folder.is_dir(): raise RuntimeError('Output path must be a folder ({})'.format(folder.resolve()))

    class_type = get_model_type_name(entity)
    model_file = folder / f'{class_type}.java'

    domain_code_writer.create_model(model_file, get_model_type_name(entity), get_package(),
                                    _get_model_imports(entity), _get_model_fields_data(entity))

    return model_file


def get_package() -> str:
    return get_config().domain_models_pkg


def get_model_type_name(entity: Entity) -> str:
    return entity.name


def _get_model_imports(entity: Entity) -> List[str]:
    imports = []
    for field in entity.fields:
        # Exclude non owning relation side getters to avoid loops in serialization
        if not _is_used_field(field): continue
        imports += get_field_imports(field)

    return imports


def _get_model_fields_data(entity: Entity) -> List[Dict[str, str]]:
    fields_data = []
    for field in entity.fields:
        # Exclude non owning relation side getters to avoid loops in serialization
        if not _is_used_field(field): continue
        fields_data.append(_get_field_data(field))

    return fields_data


def _get_field_data(field: Field) -> Dict[str, str]:
    field_data = {
        'name': field.name
    }
    field_data.update(get_field_types(field)._asdict())

    return field_data


def _is_used_field(field: Field) -> bool:
    return not field.has_relation() or not field.relation.mapped_by
