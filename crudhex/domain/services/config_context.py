from pathlib import Path
from typing import Optional

from typer import get_app_dir

from crudhex.domain.models import AppConfig
from crudhex.domain.ports import config_loader

APP_NAME = 'crudhex'
CONFIG_FILE = 'config.yaml'

_CONFIG: Optional[AppConfig] = None


def get_project_config() -> AppConfig:
    global _CONFIG
    if not _CONFIG:
        _load_project_confing()

    return _CONFIG


def set_project_config(config: AppConfig, persist: bool = False):
    """
    Set config data
    :param config: New config data
    :param persist: Persist config to file
    :return:
    """
    global _CONFIG
    _CONFIG = config

    if persist:
        persist_project_config()


def persist_project_config():
    global _CONFIG
    if not _CONFIG: return

    config_path = _get_config_path()
    config_loader.save_app_config(config_path, _CONFIG)


def _load_project_confing():
    global _CONFIG
    config_path = _get_config_path()
    if not config_path.exists():
        config_path.parent.mkdir(parents=True, exist_ok=True)
        config_path.touch()

    _CONFIG = config_loader.load_app_config(config_path)


def _get_config_path() -> Path:
    return Path(get_app_dir(APP_NAME), CONFIG_FILE)