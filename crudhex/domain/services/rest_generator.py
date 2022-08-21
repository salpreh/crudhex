from pathlib import Path
from typing import Optional

from crudhex.domain.models import Entity
from ..utils.file_utils import create_first_folder
from crudhex.domain.services.config_context import get_config
from crudhex.domain.services.rest import controller_generator


def create_model_class(entity: Entity, folder: Optional[Path] = None) -> Path:
    folder = create_first_folder(folder, Path(get_config().get_rest_controllers_path()))

    return controller_generator.create_controller_class(entity, folder)
