from abc import ABC, abstractmethod


class DatabaseFunction(ABC):
    def __init__(self, obj_db):
        self._obj_db = obj_db

    @abstractmethod
    def call(self, *args, **kwargs):
        pass

    def revert(self):
        pass
