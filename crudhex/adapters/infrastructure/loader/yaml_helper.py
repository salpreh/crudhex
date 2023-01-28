from pathlib import Path

import yaml


def load_yaml_data(path: Path) -> dict:
    config_data: dict = {}
    with open(path.resolve(), 'r', encoding='utf-8') as f:
        config_data = yaml.safe_load(f)

    return config_data if config_data else {}


def save_yaml_data(path: Path, data: dict):
    with open(path.resolve(), 'w', encoding='utf-8') as f:
        yaml.safe_dump(data, f)
