from abc import ABC
from jsonschema import validate, ValidationError


class AbstractSchema(ABC):

    def __init__(self, value):
        self.value = value
        super().__init__()

    @property
    def schema(self):
        return self.schema

    def get_schema(self):
        return self.schema

    @classmethod
    def validate(cls, data: dict):
        try:
            validate(data, cls.get_schema(cls))
            return True, None
        except ValidationError as e:
            return False, e.message
