from pathlib import Path
from typing import Dict, Optional

from crudhex.domain.utils.package_utils import pkg_to_path


class ProjectConfig:
    src: Optional[str]
    _domain_src: Optional[str]
    _db_adapter_src: Optional[str]
    _rest_adapter_src: Optional[str]

    domain_models_pkg: str
    domain_commands_pkg: str
    domain_in_ports_pkg: str
    domain_out_ports_pkg: str

    db_models_pkg: str
    db_repositories_pkg: str

    rest_models_pkg: str

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

        self.db_models_pkg = ''
        self.db_repositories_pkg = ''

        self.rest_models_pkg = ''

    @classmethod
    def from_dict(cls, data: Dict[str, str]) -> 'ProjectConfig':
        project_config = ProjectConfig()

        data = ProjectConfig._process_config(data)
        project_config.__dict__.update(**data)

        return project_config

    def get_domain_models_path(self) -> Path:
        return pkg_to_path(self.domain_models_pkg, self.domain_src)

    def get_domain_commands_path(self) -> Path:
        return pkg_to_path(self.domain_commands_pkg, self.domain_src)

    def get_domain_in_ports_path(self) -> Path:
        return pkg_to_path(self.domain_in_ports_pkg, self.domain_src)

    def get_domain_out_ports_path(self) -> Path:
        return pkg_to_path(self.domain_out_ports_pkg, self.domain_src)

    def get_domain_use_cases_path(self) -> Path:
        return pkg_to_path(self.domain_use_cases_pkg, self.domain_src)

    def get_db_models_path(self) -> Path:
        return pkg_to_path(self.db_models_pkg, self.db_adapter_src)

    def get_db_repositories_path(self) -> Path:
        return pkg_to_path(self.db_repositories_pkg, self.db_adapter_src)

    def get_rest_models_path(self) -> Path:
        return pkg_to_path(self.rest_models_pkg, self.rest_adapter_src)

    @property
    def domain_src(self):
        if self._domain_src is None:
            return self.src

        return self._domain_src

    @domain_src.setter
    def domain_src(self, src: str):
        self._domain_src = src

    @property
    def db_adapter_src(self):
        if self._db_adapter_src is None:
            return self.src

        return self._db_adapter_src

    @db_adapter_src.setter
    def db_adapter_src(self, src: str):
        self._db_adapter_src = src

    @property
    def rest_adapter_src(self):
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


class ConfigKeys:
    SOURCE = 'src'
    DOMAIN_SOURCE = 'domain-src'
    DB_SOURCE = 'db-adapter-src'
    REST_SOURCE = 'rest-adapter-src'

    DOMAIN_MODELS_PKG = 'domain-models-pkg'
    DB_MODELS_PKG = 'db-models-pkg'
    DB_REPOSITORIES_PKG = 'db-repositories-pkg'
    REST_MODELS_PKG = 'rest-models-pkg'
