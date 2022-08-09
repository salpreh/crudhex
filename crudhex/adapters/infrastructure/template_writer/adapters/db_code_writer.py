from pathlib import Path
from typing import Dict, List, Optional, Union

from crudhex.domain.models import RelationType
from crudhex.adapters.infrastructure.template_writer.config import template_config
from crudhex.adapters.infrastructure.template_writer.config.template_config import get_db_file_path
from crudhex.adapters.infrastructure.template_writer.services.template_env import get_template_environment


def create_entity(dest: Path, class_type: str, package: str,
                  imports: List[str], meta: Dict[str, str], fields: List[Dict[str, str]]):

    template_env = get_template_environment()

    id_field = _get_id_field(fields)
    if not id_field: raise RuntimeError('Id field is mandatory for db entity generation')

    fields_fragment = _generate_fields_fragment(fields)
    # TODO: Inverted relation sync accessors

    entity_template = template_env.get_template(get_db_file_path(template_config.DB_ENTITY_TEMPLATE))
    entity_code = entity_template.render({
        'package': package,
        'imports': '\n'.join(imports),
        'class_type': class_type,
        'fields': fields_fragment,
        'collection_methods': '',  # TODO
        'id_field': id_field['name'],
        **meta
    })

    with open(dest.resolve(), 'w+', encoding='utf-8') as f:
        f.write(entity_code)


def create_entity_repository(dest: Path, class_type: str, package: str,
                             imports: List[str], entity_type: str, id_type: str):

    template_env = get_template_environment()

    repository_template = template_env.get_template(get_db_file_path(template_config.DB_REPOSITORY_TEMPLATE))
    repository_code = repository_template.render({
        'package': package,
        'imports': '\n'.join(imports),
        'class_type': class_type,
        'entity_type': entity_type,
        'id_type': id_type
    })

    with open(dest.resolve(), 'w+', encoding='utf-8') as f:
        f.write(repository_code)


def _generate_fields_fragment(fields: List[Dict[str, Union[str, RelationType]]]) -> str:
    template_env = get_template_environment()

    templates = {}
    field_fragments = []
    for field in fields:
        if field['relationship']:
            template_name = template_config.get_relation_template(field['relationship'], field['mapped_by'] is None)
            template = templates.setdefault(
                template_name,
                template_env.get_template(get_db_file_path(template_name))
            )

            field_fragments.append(template.render(field))
        else:
            template = templates.setdefault(
                template_config.FIELD,
                template_env.get_template(get_db_file_path(template_config.FIELD))
            )

            field_fragments.append(template.render(field))

    return '\n\n'.join(field_fragments)


def _get_id_field(fields: List[Dict[str, str]]) -> Optional[Dict[str, str]]:
    id_field = None
    for field in fields:
        if field['id']:
            id_field = field
            break

    return id_field
