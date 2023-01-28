from pathlib import Path

from .yaml_helper import load_yaml_data

from crudhex.domain.models import ProjectConfig


def load_project_config(path: Path) -> ProjectConfig:
    config_data = load_yaml_data(path)

    return ProjectConfig.from_dict(config_data)


def load_spec_config(path: Path) -> dict:
    return load_yaml_data(path)
