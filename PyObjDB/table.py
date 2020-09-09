import json
import uuid

from PyObjDB.helpers import serialization
from PyObjDB import exceptions


class Table:
    def __init__(self, name, content=None):
        self.name = name

        if content:
            self.content = content
        else:
            self.content = {}
        self.type = None

        self.__set_type()

    def __set_type(self, obj=None):
        if obj:
            self.type = type(obj)
        else:
            if len(self.content) > 0:
                self.type = type(serialization.deserialize(list(self.content.values())[0]))

    def __same_type(self, obj):
        if len(self.content) == 0:
            return True
        return type(obj) == self.type

    def serialize(self) -> str:
        """
        Convert table content to JSON string
        :return: JSON string
        """
        return json.dumps(self.content)

    def add(self, obj) -> str:
        """
        Add an object to the table
        :param obj: some obj
        :return: row_id of the new made entry
        """
        if not self.__same_type(obj):
            raise exceptions.ObjectMismatch("The object type does not match other objects in table '{}'!"
                                            .format(self.name))

        row_id = str(uuid.uuid4().hex)
        self.content.update({row_id: serialization.serialize(obj)})

        if not self.type:
            self.__set_type(obj)

        return row_id

    def set(self, key, obj) -> None:
        """
        Directly add an entry
        :param key: row_id
        :param obj: some obj
        :return:
        """
        if key not in self.content.keys():
            self.content.update({key: serialization.serialize(obj)})
        else:
            raise exceptions.EntryExists("The entry with id '{}' already exists!".format(key))

    def get(self, key=None, filter_func=None) -> dict:
        """
        Get one, multiple or all entries.
        :param key: row_id
        :param filter_func: function to filter entries
        :return:
        """
        decoded = {}

        if key:
            decoded = {key: serialization.deserialize(self.content[key])}
        else:
            for obj_key, obj in self.content.items():
                dec = serialization.deserialize(obj)

                if filter_func:
                    if filter_func(dec):
                        decoded.update({obj_key: dec})
                else:
                    decoded.update({obj_key: dec})

        return decoded

    def delete(self, key=None, filter_func=None) -> None:
        """
        Delete one or more entries
        :param key: row_id
        :param filter_func: function to filter entries
        :return:
        """
        if key:
            self.content.pop(key)
        elif filter_func:
            for key, obj in self.get(filter_func=filter_func).items():
                self.content.pop(key)

    def update(self, new_obj, key=None, filter_func=None) -> None:
        """
        Update one or multiple entries
        :param new_obj: the obj to replace with
        :param key: row_id
        :param filter_func: function to filter entries
        :return:
        """
        if not self.__same_type(new_obj):
            raise exceptions.ObjectMismatch("The object type does not match other objects in table '{}'!"
                                            .format(self.name))

        if key:
            self.content[key] = serialization.serialize(new_obj)
        elif filter_func:
            for obj_key, obj in self.get(filter_func=filter_func).items():
                self.content[obj_key] = serialization.serialize(new_obj)

    def clear(self) -> None:
        """
        Clear the table
        :return:
        """
        self.content = {}


if __name__ == "__main__":
    table = Table("test")

    table.add([1, 2, 3])
    table.add([1, 2, 3])
    table.add([1, 2])

    print(table.get())
    table.delete(filter_func=lambda o: len(o) == 3)
    print(table.get())
