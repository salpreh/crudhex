from typing import Dict


class TypeResolver:
    type_data: Dict[str, str]

    def __init__(self, additional_types: Dict[str, str] = None):
        self.type_data = {}
        self._init()

        if additional_types:
            self.type_data.update(**additional_types)

    def resolve_type(self, class_type: str):
        return self.type_data.get(class_type, class_type)

    def _init(self):
        type_data = {
            'Collection': 'java.util.Collection',
            'List': 'java.util.List',
            'ArrayList': 'java.util.ArrayList',
            'Set': 'java.util.Set',
            'Map': 'java.util.Map',
            'HashMap': 'java.util.HashMap',
            'UUID': 'java.util.UUID',
            'Optional': 'java.util.Optional',
            'Stream': 'java.util.stream.Stream',
            'String': 'java.lang.String',
            'Double': 'java.lang.Double',
            'Float': 'java.lang.Float',
            'Integer': 'java.lang.Integer',
            'Short': 'java.lang.Short',
            'Long': 'java.lang.Long',
            'Boolean': 'java.lang.Boolean',
            'BigDecimal': 'java.math.BigDecimal',
            'BigInteger': 'java.math.BigInteger',
        }

        self.type_data.update(**type_data)