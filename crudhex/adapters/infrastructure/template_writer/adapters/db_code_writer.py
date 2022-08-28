from pathlib import Path
from typing import Dict, List, Optional, Union

from crudhex.domain.models import RelationType
from crudhex.adapters.infrastructure.template_writer.config import template_config
from crudhex.adapters.infrastructure.template_writer.config.template_config import get_db_file_path
from crudhex.adapters.infrastructure.template_writer.services.template_env import get_template_environment
from crudhex.adapters.infrastructure.template_writer.services.inflect_engine import get_inflect_engine
from . import mapper_code_writer
from crudhex.domain.models.mapper import MapperType


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


def create_adapter(dest: Path, class_type: str, package: str, class_type_interface: str,
                   imports: List[str], model_type: str, entity_type: str, id_type: str,
                   repository_type: str, create_command_type: str, update_command_type: str,
                   relations_data: List[Dict[str, str]], mapper_type: Optional[str] = None):

    template_env = get_template_environment()

    process_cmd_template = template_env.get_template(get_db_file_path(template_config.PROCESS_COMMAND))
    process_cmd_code = process_cmd_template.render({
        'entity_type': entity_type,
        'update_command_type': update_command_type,
        'command_relations': relations_data
    })

    adapter_template = template_env.get_template(get_db_file_path(template_config.DB_ADAPTER_TEMPLATE))
    adapter_code = adapter_template.render({
        'package': package,
        'imports': '\n'.join(imports),
        'class_type': class_type,
        'class_type_interface': class_type_interface,
        'main_repository_type': repository_type,
        'additional_repositories': _get_additional_repositories(relations_data, repository_type),
        'mapper_type': mapper_type,
        'model_type': model_type,
        'entity_type': entity_type,
        'id_type': id_type,
        'create_command_type': create_command_type,
        'update_command_type': update_command_type,
        'process_command': process_cmd_code
    })

    with open(dest.resolve(), 'w+', encoding='utf-8') as f:
        f.write(adapter_code)


def create_mapper(dest: Path, class_type: str, package: str,
                  imports: List[str], mappings: Dict[str, str], mapper_type: MapperType):

    mapper_code_writer.create_mapper(dest, class_type, package, imports, mappings, mapper_type)


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
            field_sing = get_inflect_engine().singular_noun(field['name'])
            params['field_sing'] = field_sing if field_sing else field['name']

        setter_fragments.append(template.render(params))

    return '\n\n'.join(setter_fragments)


def _get_id_field(fields: List[Dict[str, str]]) -> Optional[Dict[str, str]]:
    id_field = None
    for field in fields:
        if field['id']:
            id_field = field
            break

    return id_field


def _get_additional_repositories(relations_data: List[Dict[str, str]], main_repository: str) -> List[str]:
    return [rd.get('repository_type') for rd in relations_data
            if rd.get('repository_type') and rd.get('repository_type') != main_repository]
