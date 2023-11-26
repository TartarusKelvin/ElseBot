"""
For all of the things that need to ensure persistance
"""
import pathlib
import json


class Serializer:
    @staticmethod
    def serialize(data):
        raise NotImplementedError

    @staticmethod
    def deserialize(data):
        raise NotImplementedError


class JsonSerializer(Serializer):
    @staticmethod
    def serialize(data: dict) -> bytes:
        return json.dumps(data).encode("utf-8")

    @staticmethod
    def deserialize(data: bytes) -> dict:
        return json.loads(data.decode("utf-8"))


class PersistedDict:
    def __init__(
        self,
        backing_path: pathlib.Path | str,
        *,
        serializer: Serializer = JsonSerializer(),
        keyType=str,
    ):
        self._backing_path: pathlib.Path = (
            backing_path
            if isinstance(backing_path, pathlib.Path)
            else pathlib.Path(backing_path)
        )
        self._serializer = serializer
        self._dict = {}
        if self._backing_path.exists() and self._backing_path.is_file():
            data = self._serializer.deserialize(self._backing_path.read_bytes())
            self._dict = {keyType(k): v for k, v in data.items()}

    def __getitem__(self, key):
        return self._dict[key]

    def __setitem__(self, key, value):
        self._dict[key] = value
        self._save()

    def __delitem__(self, key):
        del self._dict[key]
        self._save()

    def _save(self):
        self._backing_path.write_bytes(self._serializer.serialize(self._dict))

    def items(self):
        return self._dict.items()

    def get(self, key, default):
        return self._dict.get(key, default)
