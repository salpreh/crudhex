"""
Implements `ICommonGenerator` protocol interface
"""
from pathlib import Path

from ..project_config_context import get_project_config
from ...utils.file_utils import get_java_filename

from crudhex.domain.ports import domain_code_writer

_EXCEPTION_TYPE = 'NotFoundException'


def create_class(folder: Path) -> Path:
    if not folder.is_dir(): raise RuntimeError('Output path must be a folder ({})'.format(folder.resolve()))

    model_file = folder / get_filename()

    domain_code_writer.create_exception(model_file, get_type_name(), get_package(), [])

    return model_file


def get_package() -> str:
    return get_project_config().domain_exceptions_pkg


def get_type_name() -> str:
    return _EXCEPTION_TYPE


def get_filename() -> str:
    return get_java_filename(get_type_name())
