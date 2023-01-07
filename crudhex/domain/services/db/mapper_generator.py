"""
Implements `ISharedClass` protocol interface
"""
from . import entity_generator
from ..common import mapper_generator
from ..domain import model_generator
from ..generation_commons import IGenerator
from ...utils import module_utils

_MAPPER_NAME = 'DbMapper'


def get_default_name() -> str:
    return _MAPPER_NAME


def get_from_generator() -> IGenerator:
    return entity_generator  # type: ignore


def get_to_generator() -> IGenerator:
    return model_generator  # type: ignore


# Override the default mapper generator
mapper_generator.get_default_name = get_default_name
mapper_generator.get_from_generator = get_from_generator
mapper_generator.get_to_generator = get_to_generator
mapper_generator.mapper_pkg = 'db_mapper_pkg'
mapper_generator.mapper_class = 'db_mapper_class'

module_utils.extract_functions(mapper_generator, locals())
