from collections import namedtuple
from pathlib import Path

# Pkg
from crudhex.domain.models import RelationType

TEMPLATES_PACKAGE = 'crudhex.adapters.infrastructure.template_writer'

# Base folders
TEMPLATE_FOLDER = 'templates'
DB_FOLDER = 'db'
COMMONS_FOLDER = 'commons'
FRAGMENTS_FOLDER = 'fragments'

# DB TEMPLATES
DB_ENTITY_TEMPLATE = 'entity.jinja2'
DB_REPOSITORY_TEMPLATE = 'repository.jinja2'

# DB FRAGMENTS
COLLECTION_INVERSE_METHODS = 'collection_inverse_methods.jinja2'
COLLECTION_MAIN_METHODS = 'collection_main_methods.jinja2'
FIELD = 'field.jinja2'
ID_FIELD = 'id_field.jinja2'
M2M_INVERSE_FIELD = 'm2m_inverse_field.jinja2'
M2M_MAIN_FIELD = 'm2m_main_field.jinja2'
M2ONE_FIELD = 'm2one_field.jinja2'
ONE2M_FIELD = 'one2m_field.jinja2'
ONE2ONE_MAIN_FIELD = 'one2one_main_field.jinja2'
ONE2ONE_INVERSE_FIELD = 'one2one_inverse_field.jinja2'

_FRAGMENTS = [
    COLLECTION_INVERSE_METHODS,
    COLLECTION_MAIN_METHODS,
    FIELD,
    ID_FIELD,
    M2M_INVERSE_FIELD,
    M2M_MAIN_FIELD,
    M2ONE_FIELD,
    ONE2M_FIELD,
    ONE2ONE_MAIN_FIELD,
    ONE2ONE_INVERSE_FIELD
]

RelationTemplate = namedtuple('RelationTemplate', 'main inverse')
_RELATION_TEMPLATE_MAP = {
    RelationType.ONE_TO_ONE: RelationTemplate(ONE2ONE_MAIN_FIELD, ONE2ONE_INVERSE_FIELD),
    RelationType.MANY_TO_ONE: RelationTemplate(M2ONE_FIELD, ONE2M_FIELD),
    RelationType.ONE_TO_MANY: RelationTemplate(M2ONE_FIELD, ONE2M_FIELD),  # ONE_TO_MANY always will be inverse side of relation. We keep it inverse side of template definition
    RelationType.MANY_TO_MANY: RelationTemplate(M2M_MAIN_FIELD, M2M_INVERSE_FIELD)
}


def get_db_file_path(file_name: str) -> str:
    file_path = Path(DB_FOLDER)
    if _is_fragment(file_name): file_path = file_path / FRAGMENTS_FOLDER

    return str(file_path / file_name)


def _is_fragment(file_name: str) -> bool:
    return file_name in _FRAGMENTS


def get_relation_template(relation_type: RelationType, main: bool = True):
    relation_templates = _RELATION_TEMPLATE_MAP[relation_type]

    return relation_templates.main if main else relation_templates.inverse
