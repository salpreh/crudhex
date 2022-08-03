from pathlib import Path
from typing import Optional

from crudhex.domain.models import ProjectConfig
from crudhex.adapters.infrastructure.loader.fs_spec_loader import load_project_config

DEFAULT_CONFIG = './.crudhex-conf.yaml'
_CONFIG: Optional[ProjectConfig] = None


def load_config(path: Optional[Path] = None):
    if not path: path = Path(DEFAULT_CONFIG)

    config = load_project_config(path)
    set_config(config)

    return config


def set_config(config: ProjectConfig):
    global _CONFIG
    _CONFIG = config


def get_config(default_config: Optional[ProjectConfig] = None) -> ProjectConfig:
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
