from typing import Dict


class RelationData:
    name: str
    repository_type: str
    collection_type: str
    entity_type: str
    create_command_type: str
    update_command_type: str

    def __init__(self, name: str):
        self.name = name
        self.repository_type = None
        self.collection_type = None
        self.entity_type = None
        self.create_command_type = None
        self.update_command_type = None

    def is_collection(self) -> bool:
        return bool(self.collection_type)

    def to_dict(self) -> Dict[str, str]:
        data = self.__dict__
        data['is_collection'] = self.is_collection()

        return data
