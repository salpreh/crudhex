from pathlib import Path
from typing import Optional

from crudhex.domain.models import Entity
from crudhex.domain.services.config_context import get_config
from crudhex.domain.services.domain import model_generator


def create_model_class(entity: Entity, folder: Optional[Path] = None) -> Path:
    if not folder:
        folder = Path(get_config().get_domain_models_path())

    return model_generator.create_model_class(entity, folder)
