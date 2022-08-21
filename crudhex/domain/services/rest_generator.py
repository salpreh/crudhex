from pathlib import Path
from typing import Optional, Tuple

from crudhex.domain.models import Entity
from .generation_commons import create_class
from crudhex.domain.services.config_context import get_config
from crudhex.domain.services.rest import controller_generator


def create_model_class(entity: Entity, override: bool = False, folder: Optional[Path] = None) -> Tuple[bool, Path]:
    return create_class(controller_generator, entity, override=override,
                        folder=folder, default_folder=Path(get_config().get_rest_controllers_path()))
