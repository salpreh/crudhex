from pathlib import Path
from typing import Dict

from crudgen.domain.utils.package_utils import pkg_to_path


class ProjectConfig:
    src: str
    _domain_src: str
    _db_adapter_src: str
    _rest_adapter_src: str

    domain_models_pkg: str
    db_models_pkg: str
    rest_models_pkg: str

    def __init__(self, domain_pkg: str, db_pkg: str, rest_pkg):
        self.domain_models_pkg = domain_pkg
        self.db_models_pkg = db_pkg
        self.rest_models_pkg = rest_pkg

    @classmethod
    def from_dict(cls, data: Dict[str, str]) -> 'ProjectConfig':
        project_config = ProjectConfig()
        project_config.__dict__.update(**data)

        return project_config

    def get_domain_models_path(self) -> Path:
        return pkg_to_path(self.domain_models_pkg, self.domain_src)

    def get_db_models_path(self) -> Path:
        return pkg_to_path(self.db_models_pkg, self.db_adapter_src)

    def get_rest_models_path(self) -> Path:
        return pkg_to_path(self.rest_models_pkg, self._rest_adapter_src)

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


class ConfigKeys:
    SOURCE = 'src'
    DOMAIN_SOURCE = 'domain-src'
    DB_SOURCE = 'db-adapter-src'
    REST_SOURCE = 'rest-adapter-src'

    DOMAIN_MODELS_PKG = 'domain-models-pkg'
    DB_MODELS_PKG = 'db-models-pkg'
    REST_MODELS_PKG = 'rest-models-pkg'