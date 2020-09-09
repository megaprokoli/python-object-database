from PyObjDB.db_functions.db_function import DatabaseFunction


class DBDeleteTable(DatabaseFunction):
    def __init__(self, obj_db):
        super().__init__(obj_db)
        self._table = None

    def call(self, table_name):
        self._table = self._obj_db.tables.pop(table_name)

    def revert(self):
        self._obj_db.tables.update({self._table.name: self._table})
