import pytest

from crudhex.domain.models.project_config import ProjectConfig, ConfigValidationError
from tests.utils.file_utils import load_config_fixture_file

MULTI_MOD = 'multi_mod.yaml'
MULTI_MOD_MISSING = 'multi_mod_missing_src.yaml'
MULTI_MOD_NOT_EXISTS = 'multi_mod_not_exists_src.yaml'
SINGLE_MOD = 'single_mod.yaml'
SINGLE_MOD_MISSING = 'single_mod_missing_src.yaml'


def test_load_single_mod():
    # given
    config = _load_config(SINGLE_MOD)

    # when
    config.validate()

    # then
    assert 'tests/fixtures' == config.domain_src
    assert 'tests/fixtures' == config.db_adapter_src
    assert 'tests/fixtures' == config.rest_adapter_src


def test_load_single_mod_missing_src_raise_error():
    # given
    config = _load_config(SINGLE_MOD_MISSING)

    # when
    with pytest.raises(ConfigValidationError) as err:
        config.validate()

    # then
    errors = err.value.errors
    assert 3 == len(errors)
    assert 'None' in errors[0]
    assert 'None' in errors[1]
    assert 'None' in errors[2]


def tests_load_multi_mod():
    # given
    config = _load_config(MULTI_MOD)

    # when
    config.validate()

    # then
    assert 'tests' == config.domain_src
    assert 'tests/fixtures/specs' == config.db_adapter_src
    assert 'tests/fixtures/configs' == config.rest_adapter_src


def test_load_multi_mod_missing_src_raise_error():
    # given
    config = _load_config(MULTI_MOD_MISSING)

    # when
    with pytest.raises(ConfigValidationError) as err:
        config.validate()

    # then
    errors = err.value.errors
    assert 2 == len(errors)
    assert 'None' in errors[0]
    assert 'None' in errors[1]


def test_load_multi_mod_not_exists_src_raise_error():
    # given
    config = _load_config(MULTI_MOD_NOT_EXISTS)

    # when
    with pytest.raises(ConfigValidationError) as err:
        config.validate()

    # then
    errors = err.value.errors
    assert 2 == len(errors)
    assert 'db/src/main/java' in errors[0]
    assert 'rest/src/main/java' in errors[1]


def _load_config(file: str) -> ProjectConfig:
    config_data = load_config_fixture_file(file)

    return ProjectConfig.from_dict(config_data)
