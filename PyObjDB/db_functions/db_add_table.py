from PyObjDB.db_functions.db_function import DatabaseFunction
from PyObjDB.table import Table
from PyObjDB import exceptions


class DBAddTable(DatabaseFunction):
    def __init__(self, obj_db):
        super().__init__(obj_db)
        self._table_name = None

    def call(self, table_name):
        if table_name not in self._obj_db.tables.keys():
            self._obj_db.tables.update({table_name: Table(table_name)})
            self._table_name = table_name
        else:
            raise exceptions.TableAlreadyExists("The table '{}' already exists!".format(table_name))

    def revert(self):
        self._obj_db.tables.pop(self._table_name)
