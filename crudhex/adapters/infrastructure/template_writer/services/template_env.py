from typing import Optional

from jinja2 import Environment, PackageLoader


_TEMPLATE_ENV: Optional[Environment] = None


def get_template_environment():
    global _TEMPLATE_ENV
    if _TEMPLATE_ENV: return _TEMPLATE_ENV

    _TEMPLATE_ENV = Environment(loader=PackageLoader('crudhex.adapters.infrastructure.template_writer', 'templates'),
                                trim_blocks=True, lstrip_blocks=True)

    return _TEMPLATE_ENV
