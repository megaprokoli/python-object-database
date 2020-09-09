import json

from PyObjDB import exceptions

import PyObjDB.helpers.encryption as crypto
from PyObjDB.table import Table

from PyObjDB.db_functions.db_add_table import DBAddTable
from PyObjDB.db_functions.db_add import DBAdd
from PyObjDB.db_functions.db_delete_table import DBDeleteTable
from PyObjDB.db_functions.db_delete import DBDelete
from PyObjDB.db_functions.db_update import DBUpdate
from PyObjDB.db_functions.db_clear_table import DBClearTable


# TODO integrity checks (hashing)


class PyObjDatabase:
    def __init__(self, db_dir, name, crypt_key=None):
        self.db_dir = db_dir
        self.name = name
        self.crypt_key = crypt_key

        self.tables = {}
        self.commit_queue = []
        self.manifest = self.__load_manifest()

        if self.manifest:
            self.__load_tables()

    @property
    def manifest_path(self):
        return "{}/{}.json".format(self.db_dir, self.name)

    def __load_manifest(self):
        try:
            return json.load(open(self.manifest_path, "r"))
        except FileNotFoundError:
            return None

    def __load_tables(self):
        for table_name in self.manifest["tables"]:
            with open("{}/{}.json".format(self.db_dir, table_name), "rb") as f:
                json_bytes = f.read()

            if self.crypt_key:
                json_str = crypto.decrypt(self.crypt_key, json_bytes)
            else:
                json_str = json_bytes.decode("utf-8")

            table = Table(table_name, json.loads(json_str))

            self.tables.update({table_name: table})

    def __save_manifest(self):
        self.manifest["tables"] = list(self.tables.keys())
        json.dump(self.manifest, open(self.manifest_path, "w+"))

    def __save_tables(self):
        for t in self.tables.values():
            file_path = self.db_dir + "/" + t.name + ".json"

            json_str = json.dumps(t.content)

            if self.crypt_key:
                json_bytes = crypto.encrypt(self.crypt_key, json_str)
            else:
                json_bytes = json_str.encode()

            with open(file_path, "wb+") as f:
                f.write(json_bytes)

    def __call_db_function(self, func_class, *args, **kwargs):
        func = func_class(self)
        self.commit_queue.append(func)

        func.call(*args, **kwargs)

    def commit(self) -> None:
        """
        Commit the changes made and write them to disc.
        :return:
        """
        self.__save_tables()
        self.__save_manifest()

        self.commit_queue = []

    def revert(self) -> None:  # TODO make better (without if)
        """
        Undo all changes made until the last commit.
        :return:
        """
        if len(self.commit_queue) == 1:
            self.commit_queue[0].revert()
            self.commit_queue.pop(0)
        else:
            for i in range(len(self.commit_queue) - 1, -1, -1):
                self.commit_queue[i].revert()
                self.commit_queue.pop(i)

    def create(self):
        """
        Create a new database
        :return:
        """
        self.manifest = {"db_name": self.name,
                         "tables": []}
        json.dump(self.manifest, open(self.manifest_path, "w+"))

    def get(self, table_name, row_id=None, filter_func=None) -> dict:
        """
        Get one, multiple or all entries from the given table
        :param table_name:
        :param row_id: row_id
        :param filter_func: function to filter entries
        :return:
        """
        try:
            return self.tables[table_name].get(row_id, filter_func)
        except KeyError:
            raise exceptions.TableDoesNotExist("The table '{}' does not exist yet!".format(table_name))

    def add_table(self, table_name):
        self.__call_db_function(DBAddTable, table_name)

    def delete_table(self, table_name):
        self.__call_db_function(DBDeleteTable, table_name)

    def clear_table(self, table_name):
        self.__call_db_function(DBClearTable, table_name)

    def add(self, table_name, obj):
        self.__call_db_function(DBAdd, table_name, obj)

    def delete(self, table_name, row_id=None, filter_func=None):
        self.__call_db_function(DBDelete, table_name, row_id, filter_func)

    def update(self, table_name, new_obj, row_id=None, filter_func=None):
        self.__call_db_function(DBUpdate, table_name, new_obj, row_id, filter_func)
