from pathlib import Path
from typing import Optional, Tuple, Dict

from crudhex.domain.models import Entity
from .generation_commons import create_class, create_shared_class
from crudhex.domain.services.config_context import get_config
from crudhex.domain.services.rest import controller_generator, model_generator, mapper_generator
from ..models.mapper import MapperType


def create_controller_class(entity: Entity, override: bool = False,
                            with_mapper: bool = True, folder: Optional[Path] = None) -> Tuple[bool, Path]:
    return create_class(controller_generator, entity, with_mapper, override=override,
                        folder=folder, default_folder=Path(get_config().get_rest_controllers_path()))


def create_model_class(entity: Entity, override: bool = False, folder: Optional[Path] = None) -> Tuple[bool, Path]:
    return create_class(model_generator, entity, override=override,
                        folder=folder, default_folder=Path(get_config().get_rest_models_path()))


def create_mapper_class(entities_map: Dict[str, Entity], mapper_type: MapperType,
                        override: bool = False, folder: Optional[Path] = None):
    return create_shared_class(mapper_generator, entities_map, mapper_type,
                               override=override, folder=folder, default_folder=Path(get_config().get_rest_mapper_path()))
