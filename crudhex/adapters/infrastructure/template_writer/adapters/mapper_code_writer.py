from pathlib import Path
from typing import Dict, List, Optional

from crudhex.adapters.infrastructure.template_writer.config import template_config
from crudhex.adapters.infrastructure.template_writer.config.template_config import get_mapper_file_path
from crudhex.adapters.infrastructure.template_writer.services.template_env import get_template_environment
from crudhex.domain.models.mapper import MapperType


_MAPPERS_MAP = {
    MapperType.NONE: None,
    MapperType.MAPSTRUCT: template_config.MAPSTRUCT_TEMPLATE,
    MapperType.MODELMAPPER: None
}


def create_mapper(dest: Path, class_type: str, package: str,
                  imports: List[str], mappings: Dict[str, str], mapper_type: MapperType):

    if not _has_mapper(mapper_type): return

    template_env = get_template_environment()
    template = _get_mapper_template(mapper_type)
    if not template: return  # TODO: Exception?

    mapper_template = template_env.get_template(get_mapper_file_path(template))
    mapper_code = mapper_template.render({
        'package': package,
        'imports': '\n'.join(imports),
        'class_type': class_type,
        'mappings': mappings
    })

    with open(dest.resolve(), 'w+', encoding='utf-8') as f:
        f.write(mapper_code)


def _get_mapper_template(mapper_type: MapperType) -> Optional[str]:
    return _MAPPERS_MAP.get(mapper_type)


def _has_mapper(mapper_type: MapperType) -> bool:
    return mapper_type != MapperType.NONE
