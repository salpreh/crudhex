from pathlib import Path
from typing import Dict, Optional, List

from crudhex.domain.utils.package_utils import pkg_to_path, get_package


class ProjectConfig:
    src: Optional[str]
    _domain_src: Optional[str]
    _db_adapter_src: Optional[str]
    _rest_adapter_src: Optional[str]

    domain_models_pkg: str
    domain_commands_pkg: str
    domain_in_ports_pkg: str
    domain_out_ports_pkg: str
    domain_use_cases_pkg: str
    domain_exceptions_pkg: str

    db_models_pkg: str
    db_repositories_pkg: str
    db_adapters_pkg: str
    db_mapper_pkg: str
    db_mapper_class: Optional[str]

    rest_models_pkg: str
    rest_controllers_pkg: str
    rest_exception_handler_pkg: str
    rest_mapper_pkg: str
    rest_mapper_class: Optional[str]

    def __init__(self):
        self.src = None
        self._domain_src = None
        self._db_adapter_src = None
        self._rest_adapter_src = None

        self.domain_models_pkg = ''
        self.domain_commands_pkg = ''
        self.domain_in_ports_pkg = ''
        self.domain_out_ports_pkg = ''
        self.domain_use_cases_pkg = ''
        self.domain_exceptions_pkg = ''

        self.db_models_pkg = ''
        self.db_repositories_pkg = ''
        self.db_adapters_pkg = ''
        self.db_mapper_pkg = ''
        self.db_mapper_class = None

        self.rest_models_pkg = ''
        self.rest_controllers_pkg = ''
        self.rest_exception_handler_pkg = ''
        self.rest_mapper_pkg = ''
        self.rest_mapper_class = None

    @classmethod
    def from_dict(cls, data: Dict[str, str]) -> 'ProjectConfig':
        project_config = ProjectConfig()

        data = ProjectConfig._process_config(data)
        for attr, val in data.items():
            project_config.__setattr__(attr, val)

        return project_config

    def validate(self):
        errors = []
        if not self.domain_src or not Path(self.domain_src).exists():
            errors.append(f'Unable to resolve domain src folder ({self.domain_src})')
        if not self.db_adapter_src or not Path(self.db_adapter_src).exists():
            errors.append(f'Unable to resolve db adapter src folder ({self.db_adapter_src})')
        if not self.rest_adapter_src or not Path(self.rest_adapter_src).exists():
            errors.append(f'Unable to resolve rest adapter src folder ({self.rest_adapter_src})')

        if errors: raise ConfigValidationError(errors)

    def get_domain_models_path(self) -> Path:
        return self._domain_pkg_path(self.domain_models_pkg)

    def get_domain_commands_path(self) -> Path:
        return self._domain_pkg_path(self.domain_commands_pkg)

    def get_domain_in_ports_path(self) -> Path:
        return self._domain_pkg_path(self.domain_in_ports_pkg)

    def get_domain_out_ports_path(self) -> Path:
        return self._domain_pkg_path(self.domain_out_ports_pkg)

    def get_domain_use_cases_path(self) -> Path:
        return self._domain_pkg_path(self.domain_use_cases_pkg)

    def get_domain_exceptions_path(self) -> Path:
        return self._domain_pkg_path(self.domain_exceptions_pkg)

    def get_db_models_path(self) -> Path:
        return self._db_pkg_path(self.db_models_pkg)

    def get_db_repositories_path(self) -> Path:
        return self._db_pkg_path(self.db_repositories_pkg)

    def get_db_adapters_path(self) -> Path:
        return self._db_pkg_path(self.db_adapters_pkg)

    def get_db_mapper_path(self) -> Path:
        if self.db_mapper_class: mapper_pkg = get_package(self.db_mapper_class)
        else: mapper_pkg = self.db_mapper_pkg

        return self._domain_pkg_path(mapper_pkg)

    def get_rest_models_path(self) -> Path:
        return self._rest_pkg_path(self.rest_models_pkg)

    def get_rest_controllers_path(self) -> Path:
        return self._rest_pkg_path(self.rest_controllers_pkg)

    def get_rest_exception_handler_path(self) -> Path:
        return self._rest_pkg_path(self.rest_exception_handler_pkg)

    def get_rest_mapper_path(self) -> Path:
        if self.rest_mapper_class: mapper_pkg = get_package(self.rest_mapper_class)
        else: mapper_pkg = self.rest_mapper_pkg

        return self._rest_pkg_path(mapper_pkg)

    @property
    def domain_src(self) -> Optional[str]:
        if self._domain_src is None:
            return self.src

        return self._domain_src

    @domain_src.setter
    def domain_src(self, src: str):
        self._domain_src = src

    @property
    def db_adapter_src(self) -> Optional[str]:
        if self._db_adapter_src is None:
            return self.src

        return self._db_adapter_src

    @db_adapter_src.setter
    def db_adapter_src(self, src: str):
        self._db_adapter_src = src

    @property
    def rest_adapter_src(self) -> Optional[str]:
        if self._rest_adapter_src is None:
            return self.src

        return self._rest_adapter_src

    @rest_adapter_src.setter
    def rest_adapter_src(self, src: str):
        self._rest_adapter_src = src

    @classmethod
    def _process_config(cls, config_data: Dict[str, str]) -> Dict[str, str]:
        p_config = {}
        for key, val in config_data.items():
            p_config[key.replace('-', '_')] = val

        return p_config

    def _domain_pkg_path(self, pkg: str) -> Path:
        return pkg_to_path(pkg, self.domain_src)

    def _db_pkg_path(self, pkg: str) -> Path:
        return pkg_to_path(pkg, self.db_adapter_src)

    def _rest_pkg_path(self, pkg: str) -> Path:
        return pkg_to_path(pkg, self.rest_adapter_src)


class ConfigValidationError(RuntimeError):
    _errors: List[str]

    def __init__(self, errors=None):
        super().__init__(','.join(errors) if errors else None)
        self._errors = errors

    @property
    def errors(self) -> List[str]:
        return self._errors
