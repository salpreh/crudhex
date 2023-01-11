from pathlib import Path
from typing import List, Dict

from crudhex.adapters.infrastructure.template_writer.config import template_config
from crudhex.adapters.infrastructure.template_writer.config.template_config import get_rest_file_path
from crudhex.adapters.infrastructure.template_writer.services.template_env import get_template_environment


def create_controller(dest: Path, class_type: str, package: str,
                      imports: List[str], entity_name: str, model_type: str,
                      id_type: str, use_case_type: str, mapper_type: str,
                      create_command_type: str, update_command_type: str, as_page: bool):

    template_env = get_template_environment()

    template_name = template_config.CONTROLLER_WITH_MAP_TEMPLATE if mapper_type else template_config.CONTROLLER_TEMPLATE
    controller_template = template_env.get_template(get_rest_file_path(template_name))
    controller_code = controller_template.render({
        'package': package,
        'imports': '\n'.join(imports),
        'class_type': class_type,
        'name': entity_name,
        'use_case_type': use_case_type,
        'model_type': model_type,
        'id_type': id_type,
        'mapper_type': mapper_type,
        'create_command_type': create_command_type,
        'update_command_type': update_command_type,
        'as_page': as_page
    })

    with open(dest.resolve(), 'w+', encoding='utf-8') as f:
        f.write(controller_code)


def create_exception_handler(dest: Path, class_type: str, package: str, imports: List[str], not_found_exception_type: str):

    template_env = get_template_environment()

    exception_handler_template = template_env.get_template(get_rest_file_path(template_config.EXCEPTION_HANDLER_TEMPLATE))
    api_exception_handler_code = exception_handler_template.render({
        'package': package,
        'imports': '\n'.join(imports),
        'class_type': class_type,
        'not_found_exception_type': not_found_exception_type
    })

    with open(dest.resolve(), 'w+', encoding='utf-8') as f:
        f.write(api_exception_handler_code)


def create_model(dest: Path, class_type: str, package: str,
                 imports: List[str], fields: List[Dict[str, str]]):

    template_env = get_template_environment()

    fields_fragment = _generate_fields_fragment(fields)

    model_template = template_env.get_template(get_rest_file_path(template_config.REST_MODEL_TEMPLATE))
    model_code = model_template.render({
        'package': package,
        'imports': '\n'.join(imports),
        'class_type': class_type,
        'fields': fields_fragment
    })

    with open(dest.resolve(), 'w+', encoding='utf-8') as f:
        f.write(model_code)


def _generate_fields_fragment(fields: List[Dict[str, str]]) -> str:
    template_env = get_template_environment()
    field_template = template_env.get_template(get_rest_file_path(template_config.REST_FIELD))

    field_fragments = []
    for field in fields:
        field_fragments.append(field_template.render(**field))

    return ''.join(field_fragments)
