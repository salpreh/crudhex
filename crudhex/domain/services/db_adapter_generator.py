from pathlib import Path
from typing import Optional, Dict

from .db import entity_generator, repository_generator, adapter_generator
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


def create_adapter_class(entity: Entity, entities_map: Dict[str, Entity], folder: Optional[Path] = None) -> Path:
    if not folder:
        folder = Path(get_config().get_db_adapters_path())

    return adapter_generator.create_adapter_class(entity, entities_map, folder)
