from typing import Dict, Any


class AppConfig:
    templates: Dict[str, str]

    def __init__(self):
        self.templates = {}

    @classmethod
    def from_dict(cls, config_data: Dict[str, Any]) -> 'AppConfig':
        app_config = AppConfig()
        app_config.templates = config_data.get('templates', {})

        return app_config

    def to_dict(self) -> Dict[str, Any]:
        return {
            'templates': self.templates
        }
