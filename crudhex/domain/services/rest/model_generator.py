from pathlib import Path
from typing import List, Dict

from crudhex.domain.models import Entity, Field
from crudhex.domain.utils.class_type_utils import get_field_imports, get_field_types
from crudhex.domain.utils.file_utils import get_java_filename
from ..project_config_context import get_project_config

from crudhex.domain.ports import rest_code_writer

_REST_MODEL_SUFFIX = 'Dto'


def create_class(entity: Entity, folder: Path) -> Path:
    if not folder.is_dir(): raise RuntimeError('Output path must be a folder ({})'.format(folder.resolve()))

    model_file = folder / get_filename(entity)

    rest_code_writer.create_model(model_file, get_type_name(entity), get_package(),
                                  _get_imports(entity), _get_model_fields_data(entity))

    return model_file


def get_package() -> str:
    return get_project_config().rest_models_pkg


def get_type_name(entity: Entity) -> str:
    return _get_model_type_name(entity.name)


def get_filename(entity: Entity) -> str:
    return get_java_filename(get_type_name(entity))


def _get_model_type_name(class_type: str) -> str:
    return f'{class_type}{_REST_MODEL_SUFFIX}'


def _get_imports(entity: Entity) -> List[str]:
    imports = set()
    for field in entity.fields:
        # Exclude non owning relation side getters to avoid loops in serialization
        if not _is_used_field(field): continue
        imports.update(set(get_field_imports(field)))

    return list(imports)


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

    if field.type.is_generated:
        field_data['class_type'] = _get_model_type_name(field_data['class_type'])

    return field_data


def _is_used_field(field: Field) -> bool:
    return not field.has_relation() or not field.relation.mapped_by
