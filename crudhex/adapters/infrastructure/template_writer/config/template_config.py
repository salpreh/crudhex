from collections import namedtuple
from pathlib import Path
from typing import Optional

from crudhex.domain.models import RelationType

# Pkg
TEMPLATES_PACKAGE = 'crudhex.adapters.infrastructure.template_writer'

# Base folders
TEMPLATE_FOLDER = 'templates'
DOMAIN_FOLDER = 'domain'
DB_FOLDER = 'db'
REST_FOLDER = 'rest'
COMMONS_FOLDER = 'commons'
FRAGMENTS_FOLDER = 'fragments'
MAPPERS_FOLDER = 'mappers'

# DOMAIN TEMPLATES
MODEL_TEMPLATE = 'model.jinja2'
COMMAND_TEMPLATE = 'command.jinja2'
DB_PORT_TEMPLATE = 'db_port.jinja2'
USE_CASE_PORT_TEMPLATE = 'use_case_port.jinja2'
USE_CASE_TEMPLATE = 'use_case.jinja2'
EXCEPTION_TEMPLATE = 'exception.jinja2'

# DOMAIN FRAGMENTS
DOM_FIELD = 'field.jinja2'

# DB TEMPLATES
DB_ENTITY_TEMPLATE = 'entity.jinja2'
DB_REPOSITORY_TEMPLATE = 'repository.jinja2'
DB_ADAPTER_TEMPLATE = 'adapter.jinja2'

# DB FRAGMENTS
FIELD = 'field.jinja2'
ID_FIELD = 'id_field.jinja2'
M2M_INVERSE_FIELD = 'm2m_inverse_field.jinja2'
M2M_MAIN_FIELD = 'm2m_main_field.jinja2'
M2ONE_FIELD = 'm2one_field.jinja2'
ONE2M_FIELD = 'one2m_field.jinja2'
ONE2ONE_MAIN_FIELD = 'one2one_main_field.jinja2'
ONE2ONE_INVERSE_FIELD = 'one2one_inverse_field.jinja2'
M2M_SYNC_SETTER = 'm2m_sync_setter.jinja2'
ONE2M_SYNC_SETTER = 'one2m_sync_setter.jinja2'
ONE2ONE_SYNC_SETTER = 'one2one_sync_setter.jinja2'
M2X_SETTER = 'm2x_setter.jinja2'
PROCESS_COMMAND = 'process_command.jinja2'

# REST TEMPLATES
CONTROLLER_TEMPLATE = 'controller.jinja2'
CONTROLLER_WITH_MAP_TEMPLATE = 'controller_w_map.jinja2'
REST_MODEL_TEMPLATE = 'model.jinja2'
EXCEPTION_HANDLER_TEMPLATE = 'api_exception_handler.jinja2'

# REST FRAGMENTS
REST_FIELD = 'field.jinja2'

# MAPPERS TEMPLATES
MAPSTRUCT_TEMPLATE = 'mapstruct.jinja2'

_FRAGMENTS = [
    FIELD,
    ID_FIELD,
    M2M_INVERSE_FIELD,
    M2M_MAIN_FIELD,
    M2ONE_FIELD,
    ONE2M_FIELD,
    ONE2ONE_MAIN_FIELD,
    ONE2ONE_INVERSE_FIELD,
    DOM_FIELD,
    M2M_SYNC_SETTER,
    ONE2M_SYNC_SETTER,
    ONE2ONE_SYNC_SETTER,
    M2X_SETTER,
    PROCESS_COMMAND,
    REST_FIELD
]

RelationTemplate = namedtuple('RelationTemplate', 'main inverse')
_RELATION_TEMPLATE_MAP = {
    RelationType.ONE_TO_ONE: RelationTemplate(ONE2ONE_MAIN_FIELD, ONE2ONE_INVERSE_FIELD),
    RelationType.MANY_TO_ONE: RelationTemplate(M2ONE_FIELD, ONE2M_FIELD),
    RelationType.ONE_TO_MANY: RelationTemplate(M2ONE_FIELD, ONE2M_FIELD),  # ONE_TO_MANY always will be inverse side of relation. We keep it inverse side of template definition
    RelationType.MANY_TO_MANY: RelationTemplate(M2M_MAIN_FIELD, M2M_INVERSE_FIELD)
}

_RELATION_SYNC_TEMPLATE_MAP = {
    RelationType.ONE_TO_ONE: RelationTemplate(None, ONE2ONE_SYNC_SETTER),
    RelationType.MANY_TO_ONE: RelationTemplate(None, ONE2M_SYNC_SETTER),
    RelationType.ONE_TO_MANY: RelationTemplate(None, ONE2M_SYNC_SETTER),  # ONE_TO_MANY always will be inverse side of relation. We keep it inverse side of template definition
    RelationType.MANY_TO_MANY: RelationTemplate(M2X_SETTER, M2M_SYNC_SETTER)
}


def get_db_file_path(file_name: str) -> str:
    file_path = _evaluate_file_type(Path(DB_FOLDER), file_name)

    return str(file_path / file_name)


def get_domain_file_path(file_name: str) -> str:
    file_path = _evaluate_file_type(Path(DOMAIN_FOLDER), file_name)

    return str(file_path / file_name)


def get_rest_file_path(file_name: str) -> str:
    file_path = _evaluate_file_type(Path(REST_FOLDER), file_name)

    return str(file_path / file_name)


def get_mapper_file_path(file_name: str) -> str:
    file_path = _evaluate_file_type(Path(MAPPERS_FOLDER), file_name)

    return str(file_path / file_name)


def get_relation_template(relation_type: RelationType, main: bool = True) -> str:
    relation_templates = _RELATION_TEMPLATE_MAP[relation_type]

    return relation_templates.main if main else relation_templates.inverse


def get_sync_relation_template(relation_type: RelationType, main: bool = True) -> Optional[str]:
    relation_templates = _RELATION_SYNC_TEMPLATE_MAP[relation_type]

    return relation_templates.main if main else relation_templates.inverse


def _evaluate_file_type(root_path: Path, file_name: str) -> Path:
    path = root_path
    if _is_fragment(file_name): path = root_path / FRAGMENTS_FOLDER

    return path


def _is_fragment(file_name: str) -> bool:
    return file_name in _FRAGMENTS
