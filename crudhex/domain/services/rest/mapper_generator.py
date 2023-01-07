"""
Implements `ISharedClass` protocol interface
"""

from . import model_generator
from ..domain import model_generator as domain_model_generator
from ..common import mapper_generator
from ..generation_commons import IGenerator
from ...utils import module_utils

_MAPPER_NAME = 'ApiMapper'


def get_default_name() -> str:
    return _MAPPER_NAME


def get_from_generator() -> IGenerator:
    return domain_model_generator  # type: ignore


def get_to_generator() -> IGenerator:
    return model_generator  # type: ignore


# Override default mapper generator
mapper_generator.get_default_name = get_default_name
mapper_generator.get_from_generator = get_from_generator
mapper_generator.get_to_generator = get_to_generator

module_utils.extract_functions(mapper_generator, locals())
