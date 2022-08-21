from os import path
from pathlib import Path

import yaml


FIXTURE_FOLDER = 'fixtures'
SPECS_FOLDER = 'specs'
CONFIG_FOLDER = 'configs'


def load_spec_fixture_file(filename: str) -> dict:
    return load_fixture_file(path.join(SPECS_FOLDER, filename))


def load_config_fixture_file(filename: str) -> dict:
    return load_fixture_file(path.join(CONFIG_FOLDER, filename))


def load_fixture_file(filename: str) -> dict:
    fixture = {}
    with open((_get_fixture_folder_path() / filename).resolve(), 'r', encoding='utf-8') as f:
        fixture = yaml.safe_load(f)

    return fixture


def _get_fixture_folder_path() -> Path:
    return Path(__file__).parent.parent / FIXTURE_FOLDER
