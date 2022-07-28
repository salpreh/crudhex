from pathlib import Path

import yaml


FIXTURE_FOLDER = 'fixtures'


def load_fixture_file(filename: str) -> dict:
    fixture = {}
    with open((_get_fixture_folder_path() / filename).resolve(), 'r', encoding='utf-8') as f:
        fixture = yaml.safe_load(f)

    return fixture


def _get_fixture_folder_path() -> Path:
    return Path(__file__).parent.parent / FIXTURE_FOLDER
