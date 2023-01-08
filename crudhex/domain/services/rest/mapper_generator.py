"""
Implements `ISharedGenerator` protocol interface
"""
from pathlib import Path
from typing import Dict

from . import model_generator
from ..common import mapper_generator
from ..domain import model_generator as domain_model_generator
from ...models import Entity
from ...models.mapper import MapperType

_MAPPER_NAME = 'ApiMapper'
_MAPPER_CLASS_KEY = 'rest_mapper_class'
_MAPPER_PKG_KEY = 'rest_mapper_pkg'


def create_class(entities_map: Dict[str, Entity], mapper_type: MapperType, folder: Path) -> Path:
    mapper_params = mapper_generator.MapperParams(domain_model_generator, model_generator, get_package(), get_type_name()) # type: ignore
    return mapper_generator.create_class(entities_map, mapper_type, folder, mapper_params)


def get_package() -> str:
    return mapper_generator.get_package(_MAPPER_CLASS_KEY, _MAPPER_PKG_KEY)


def get_type_name() -> str:
    return mapper_generator.get_type_name(_MAPPER_CLASS_KEY, _MAPPER_NAME)


def get_filename() -> str:
    return mapper_generator.get_filename(_MAPPER_CLASS_KEY, _MAPPER_NAME)
