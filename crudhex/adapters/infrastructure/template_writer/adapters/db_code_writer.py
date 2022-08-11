from pathlib import Path
from typing import Dict, List, Optional, Union

from crudhex.domain.models import RelationType
from crudhex.adapters.infrastructure.template_writer.config import template_config
from crudhex.adapters.infrastructure.template_writer.config.template_config import get_db_file_path
from crudhex.adapters.infrastructure.template_writer.services.template_env import get_template_environment
from crudhex.adapters.infrastructure.template_writer.services.inflect_engine import get_inflect_engine


def create_entity(dest: Path, class_type: str, package: str,
                  imports: List[str], meta: Dict[str, str], fields: List[Dict[str, str]]):

    template_env = get_template_environment()

    id_field = _get_id_field(fields)
    if not id_field: raise RuntimeError('Id field is mandatory for db entity generation')

    fields_fragment = _generate_fields_fragment(fields)
    setters_fragment = _generate_fields_relation_setters(fields)

    entity_template = template_env.get_template(get_db_file_path(template_config.DB_ENTITY_TEMPLATE))
    entity_code = entity_template.render({
        'package': package,
        'imports': '\n'.join(imports),
        'class_type': class_type,
        'fields': fields_fragment,
        'methods': setters_fragment,
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


def _generate_fields_relation_setters(fields: List[Dict[str, Union[RelationType, str]]]) -> str:
    template_env = get_template_environment()

    templates = {}
    setter_fragments = []
    for field in fields:
        if not field['relationship']: continue  # Sync setters only for relations

        template_name = template_config.get_sync_relation_template(field['relationship'], field['mapped_by'] is None)
        if not template_name: continue

        template = templates.setdefault(template_name, template_env.get_template(get_db_file_path(template_name)))
        params = {**field, 'field': field['name']}
        if field['relationship'].has_multiple():
            params['field_sing'] = get_inflect_engine().singular_noun(field['name'])

        setter_fragments.append(template.render(params))

    return '\n\n'.join(setter_fragments)


def _get_id_field(fields: List[Dict[str, str]]) -> Optional[Dict[str, str]]:
    id_field = None
    for field in fields:
        if field['id']:
            id_field = field
            break

    return id_field
