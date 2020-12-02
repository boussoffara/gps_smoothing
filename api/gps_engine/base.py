import json

from schema import Schema


class BaseModel(object):
    def __init__(self, data):
        self._data = data

    def to_json(self):
        return json.dumps(self.serializable())

    def serializable(self):
        return self._data

    def valid(self):
        return self.__class__.schema().is_valid(self._data)

    def validate(self):
        return self.__class__.schema().validate(self._data)

    @classmethod
    def from_json(cls, json_string):
        data = json.loads(json_string)
        return cls(data)

    @classmethod
    def schema(cls):
        return Schema({})
