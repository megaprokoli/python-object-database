from PyObjDB.db_functions.db_function import DatabaseFunction
from PyObjDB import exceptions


class DBClearTable(DatabaseFunction):
    def __init__(self, obj_db):
        super().__init__(obj_db)
        self._table_name = None
        self._content = None

    def call(self, table_name):
        try:
            table = self._obj_db.tables[table_name]
            self._table_name = table_name
            self._content = table.content

            table.clear()
        except KeyError:
            raise exceptions.TableDoesNotExist("The table '{}' does not exists!".format(table_name))

    def revert(self):
        self._obj_db.tables[self._table_name].content = self._content
