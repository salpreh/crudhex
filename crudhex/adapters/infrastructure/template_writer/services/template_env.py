from typing import Optional

from jinja2 import Environment, PackageLoader

from ..config import template_config

_TEMPLATE_ENV: Optional[Environment] = None


def get_template_environment():
    global _TEMPLATE_ENV
    if _TEMPLATE_ENV: return _TEMPLATE_ENV

    _TEMPLATE_ENV = Environment(loader=PackageLoader(template_config.TEMPLATES_PACKAGE, template_config.TEMPLATE_FOLDER),
                                trim_blocks=True, lstrip_blocks=True)

    _TEMPLATE_ENV.filters['firstlower'] = _first_lower_filter
    _TEMPLATE_ENV.filters['firstupper'] = _first_upper_filter

    return _TEMPLATE_ENV


def _first_lower_filter(value: str) -> str:
    if not value or len(value) == 0: return value

    return value[0].lower() + value[1:]


def _first_upper_filter(value: str) -> str:
    if not value or len(value) == 0: return value

    return value[0].upper() + value[1:]
