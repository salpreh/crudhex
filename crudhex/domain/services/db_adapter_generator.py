from pathlib import Path
from typing import Optional, Dict, Tuple

from .db import entity_generator, repository_generator, adapter_generator, mapper_generator
from .project_config_context import get_project_config
from .generation_commons import create_class, create_shared_class
from crudhex.domain.models import Entity
from ..models.mapper import MapperType


def create_entity_class(entity: Entity, override: bool = False, folder: Optional[Path] = None) -> Tuple[bool, Path]:
    return create_class(entity_generator, entity, override=override,
                        folder=folder, default_folder=Path(get_project_config().get_db_models_path()))


def create_repository_class(entity: Entity, override: bool = False, folder: Optional[Path] = None) -> Tuple[bool, Path]:
    return create_class(repository_generator, entity, override=override,
                        folder=folder, default_folder=Path(get_project_config().get_db_repositories_path()))


def create_adapter_class(entity: Entity, entities_map: Dict[str, Entity],
                         override: bool = False, folder: Optional[Path] = None) -> Tuple[bool, Path]:
    return create_class(adapter_generator, entity, entities_map,
                        override=override, folder=folder, default_folder=Path(get_project_config().get_db_adapters_path()))


def create_mapper_class(entities_map: Dict[str, Entity], mapper_type: MapperType,
                        override: bool = False, folder: Optional[Path] = None):
    return create_shared_class(mapper_generator, entities_map, mapper_type,
                               override=override, folder=folder, default_folder=Path(get_project_config().get_db_mapper_path()))
