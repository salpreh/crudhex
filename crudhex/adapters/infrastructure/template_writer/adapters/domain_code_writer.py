from pathlib import Path
from typing import List, Dict, Optional

from crudhex.adapters.infrastructure.template_writer.services.template_env import get_template_environment
from crudhex.adapters.infrastructure.template_writer.config import template_config
from crudhex.adapters.infrastructure.template_writer.config.template_config import get_domain_file_path


def create_command(dest: Path, class_type: str, package: str,
                   imports: List[str], fields: List[Dict[str, str]]):

    _create_data_class(template_config.COMMAND_TEMPLATE, dest, class_type,
                       package, imports, fields)


def create_model(dest: Path, class_type: str, package: str,
                 imports: List[str], fields: List[Dict[str, str]]):

    _create_data_class(template_config.MODEL_TEMPLATE, dest, class_type,
                       package, imports, fields)


def create_db_port(dest: Path, class_type: str, package: str,
                   imports: List[str], id_type: str, model_type: str,
                   create_cmd_type: str, update_cmd_type: str):

    _create_port_class(template_config.DB_PORT_TEMPLATE, dest, class_type,
                       package, imports, id_type,
                       model_type, create_cmd_type, update_cmd_type)


def create_use_case_port(dest: Path, class_type: str, package: str,
                         imports: List[str], id_type: str, model_type: str,
                         create_cmd_type: str, update_cmd_type: str):

    _create_port_class(template_config.USE_CASE_PORT_TEMPLATE, dest, class_type,
                       package, imports, id_type,
                       model_type, create_cmd_type, update_cmd_type)


def create_use_case(dest: Path, class_type: str, package: str, class_type_interface: str,
                    imports: List[str], id_type: str, model_type: str, create_cmd_type: str,
                    update_cmd_type: str, db_port_type: str):

    extras = {'db_port_type': db_port_type, 'class_type_interface': class_type_interface}

    _create_port_class(template_config.USE_CASE_TEMPLATE, dest, class_type,
                       package, imports, id_type,
                       model_type, create_cmd_type, update_cmd_type, extras)


def create_exception(dest: Path, class_type: str, package: str, imports: List[str]):
    template_env = get_template_environment()

    exception_template = template_env.get_template(get_domain_file_path(template_config.EXCEPTION_TEMPLATE))
    exception_data = {
        'package': package,
        'imports': '\n'.join(imports),
        'class_type': class_type
    }

    exception_code = exception_template.render(exception_data)

    with open(dest.resolve(), 'w+', encoding='utf-8') as f:
        f.write(exception_code)


def _create_data_class(template: str, dest: Path, class_type: str, package: str,
                       imports: List[str], fields: List[Dict[str, str]]):

    template_env = get_template_environment()

    fields_fragment = _generate_fields_fragment(fields)

    model_template = template_env.get_template(get_domain_file_path(template))
    model_code = model_template.render({
        'package': package,
        'imports': '\n'.join(imports),
        'class_type': class_type,
        'fields': fields_fragment
    })

    with open(dest.resolve(), 'w+', encoding='utf-8') as f:
        f.write(model_code)


def _create_port_class(template: str, dest: Path, class_type: str, package: str,
                       imports: List[str], id_type: str, model_type: str,
                       create_cmd_type: str, update_cmd_type: str, extra_params: Optional[Dict[str, str]] = None):

    template_env = get_template_environment()

    port_template = template_env.get_template(get_domain_file_path(template))
    port_data = {
        'package': package,
        'imports': '\n'.join(imports),
        'class_type': class_type,
        'model_type': model_type,
        'id_type': id_type,
        'create_command_type': create_cmd_type,
        'update_command_type': update_cmd_type
    }
    if extra_params: port_data.update(**extra_params)

    port_code = port_template.render(port_data)

    with open(dest.resolve(), 'w+', encoding='utf-8') as f:
        f.write(port_code)


def _generate_fields_fragment(fields: List[Dict[str, str]]) -> str:
    template_env = get_template_environment()
    field_template = template_env.get_template(get_domain_file_path(template_config.DOM_FIELD))

    field_fragments = []
    for field in fields:
        field_fragments.append(field_template.render(**field))

    return ''.join(field_fragments)
