from pathlib import Path
from typing import List, Dict

from .services.template_env import get_template_environment
from .config import tempate_config
from .config.tempate_config import get_domain_file_path


def create_command(dest: Path, class_type: str, package: str,
                   imports: List[str], fields: List[Dict[str, str]]):

    _create_data_class(tempate_config.COMMAND_TEMPLATE, dest, class_type,
                       package, imports, fields)


def create_model(dest: Path, class_type: str, package: str,
                 imports: List[str], fields: List[Dict[str, str]]):

    _create_data_class(tempate_config.MODEL_TEMPLATE, dest, class_type,
                       package, imports, fields)


def create_db_port(dest: Path, class_type: str, package: str,
                   imports: List[str], id_type: str, model_type: str,
                   create_cmd_type: str, update_cmd_type: str):

    template_env = get_template_environment()

    port_template = template_env.get_template(get_domain_file_path(tempate_config.DB_PORT_TEMPLATE))
    port_code = port_template.render({
        'package': package,
        'imports': '\n'.join(imports),
        'class_type': class_type,
        'model_type': model_type,
        'id_type': id_type,
        'create_command_type': create_cmd_type,
        'update_command_type': update_cmd_type
    })

    with open(dest.resolve(), 'w+', encoding='utf-8') as f:
        f.write(port_code)


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


def _generate_fields_fragment(fields: List[Dict[str, str]]):
    template_env = get_template_environment()
    field_template = template_env.get_template(get_domain_file_path(tempate_config.DOM_FIELD))

    field_fragments = []
    for field in fields:
        field_fragments.append(field_template.render(**field))

    return ''.join(field_fragments)
