from pathlib import Path
from typing import Optional

from crudhex.domain.models import ProjectConfig
from crudhex.domain.ports import spec_loader

DEFAULT_CONFIG = './.crudhex-conf.yaml'
_CONFIG: Optional[ProjectConfig] = None


def load_project_config(path: Optional[Path] = None):
    if not path: path = Path(DEFAULT_CONFIG)

    config = spec_loader.load_project_config(path)
    set_project_config(config)

    return config


def set_project_config(config: ProjectConfig):
    global _CONFIG
    _CONFIG = config


def get_project_config(default_config: Optional[ProjectConfig] = None) -> ProjectConfig:
    """
    Returns config in context. If not available it will try to use provided `default_config`, otherwise will raise an exeption
    :param default_config:
    :raise RuntimeError: If no config nor default available
    :return:
    """
    global _CONFIG
    if not _CONFIG:
        if not default_config: raise RuntimeError("Config not available in context")
        else: return default_config

    return _CONFIG


def has_config() -> bool:
    global _CONFIG
    return _CONFIG is not None
