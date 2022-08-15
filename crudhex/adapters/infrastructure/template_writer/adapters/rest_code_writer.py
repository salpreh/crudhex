from pathlib import Path
from typing import List

from crudhex.adapters.infrastructure.template_writer.config import template_config
from crudhex.adapters.infrastructure.template_writer.config.template_config import get_rest_file_path
from crudhex.adapters.infrastructure.template_writer.services.template_env import get_template_environment


def create_controller(dest: Path, class_type: str, package: str,
                      imports: List[str], entity_name: str, model_type: str, id_type: str,
                      use_case_type: str, create_command_type: str, update_command_type: str):

    template_env = get_template_environment()

    repository_template = template_env.get_template(get_rest_file_path(template_config.CONTROLLER_TEMPLATE))
    repository_code = repository_template.render({
        'package': package,
        'imports': '\n'.join(imports),
        'class_type': class_type,
        'name': entity_name,
        'use_case_type': use_case_type,
        'model_type': model_type,
        'id_type': id_type,
        'create_command_type': create_command_type,
        'update_command_type': update_command_type
    })

    with open(dest.resolve(), 'w+', encoding='utf-8') as f:
        f.write(repository_code)
