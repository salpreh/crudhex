from pathlib import Path

from .yaml_helper import load_yaml_data, save_yaml_data

from crudhex.domain.models import AppConfig


def load_app_config(path: Path) -> AppConfig:
    config_data = load_yaml_data(path)

    return AppConfig.from_dict(config_data)


def save_app_config(path: Path, config: AppConfig):
    config_data = config.to_dict()
    save_yaml_data(path, config_data)
