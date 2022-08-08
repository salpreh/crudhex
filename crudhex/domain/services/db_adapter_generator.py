from pathlib import Path
from typing import Optional

from .db import entity_generator
from .db import repository_generator
from .config_context import get_config
from crudhex.domain.models import Entity


def create_entity_class(entity: Entity, folder: Optional[Path] = None) -> Path:
    if not folder:
        folder = Path(get_config().get_db_models_path())

    return entity_generator.create_entity_class(entity, folder)


def create_repository_class(entity: Entity, folder: Optional[Path] = None) -> Path:
    if not folder:
        folder = Path(get_config().get_db_repositories_path())

    return repository_generator.create_repository_class(entity, folder)
