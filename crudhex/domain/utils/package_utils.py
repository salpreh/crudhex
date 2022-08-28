from pathlib import Path
from typing import Tuple, Optional


IMPORT_TEMPLATE = 'import {};'


def pkg_to_path(pkg: str, base_path: str = '.') -> Path:
    pkg_path = pkg.replace('.', '/')

    return Path(base_path) / pkg_path


def is_full_class_name(class_name: str) -> bool:
    return len(class_name.split('.')) > 1


def get_class_name(class_name: str) -> str:
    return class_name.split('.')[-1]


def get_package(class_name: str) -> str:
    return parse_class_name(class_name)[0]


def parse_class_name(class_name: str) -> Tuple[str, str]:
    class_pkgs = class_name.split('.')

    pkg = None if len(class_pkgs) == 1 else '.'.join(class_pkgs[0:-1])
    cls_type = class_pkgs[-1]

    return pkg, cls_type


def full_class_name(pkg: Optional[str], class_type: str):
    if not pkg: return class_type

    return '.'.join((pkg, class_type))


def generate_import(full_class_name: str) -> str:
    return IMPORT_TEMPLATE.format(full_class_name)
