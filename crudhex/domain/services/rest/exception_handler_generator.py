"""
Implements `ICommonGenerator` protocol interface
"""
from pathlib import Path
from typing import List

from ..project_config_context import get_project_config
from ...utils.class_type_utils import get_import
from ...utils.file_utils import get_java_filename
from ..domain import not_found_exception_generator

from crudhex.domain.ports import rest_code_writer

_HANDLER_TYPE = 'ApiExceptionHandler'


def create_class(folder: Path) -> Path:
    if not folder.is_dir(): raise RuntimeError('Output path must be a folder ({})'.format(folder.resolve()))

    model_file = folder / get_filename()

    rest_code_writer.create_exception_handler(model_file, get_type_name(), get_package(),
                                              _get_imports(), not_found_exception_generator.get_type_name())

    return model_file


def get_package() -> str:
    return get_project_config().rest_exception_handler_pkg


def get_type_name() -> str:
    return _HANDLER_TYPE


def get_filename() -> str:
    return get_java_filename(get_type_name())


def _get_imports() -> List[str]:
    return [
        get_import(not_found_exception_generator.get_package(), not_found_exception_generator.get_type_name()),
    ]
