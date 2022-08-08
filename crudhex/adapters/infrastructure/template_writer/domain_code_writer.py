from pathlib import Path
from typing import List, Dict

from .services.template_env import get_template_environment
from .config import tempate_config
from .config.tempate_config import get_domain_file_path


def create_model(dest: Path, class_type: str, package: str,
                 imports: List[str], fields: List[Dict[str, str]]):

    template_env = get_template_environment()

    fields_fragment = _generate_fields_fragment(fields)

    model_template = template_env.get_template(get_domain_file_path(tempate_config.MODEL_TEMPLATE))
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
