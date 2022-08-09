from pathlib import Path
from typing import Optional

import yaml


from crudhex.domain.models import ProjectConfig


def load_project_config(path: Path) -> ProjectConfig:
    config_data = _load_yaml_data(path)

    return ProjectConfig.from_dict(config_data)


def load_spec_config(path: Path) -> dict:
    return _load_yaml_data(path)


def _load_yaml_data(path: Path) -> dict:
    config_data: dict = {}
    with open(path.resolve(), 'r', encoding='utf-8') as f:
        config_data = yaml.safe_load(f)

    return config_data


def _default_path(file: str) -> Path:
    return Path('.') / file
