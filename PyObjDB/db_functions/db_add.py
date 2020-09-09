from PyObjDB.db_functions.db_function import DatabaseFunction


class DBAdd(DatabaseFunction):
    def __init__(self, obj_db):
        super().__init__(obj_db)
        self._table_name = None
        self._row_id = None

    def call(self, table_name, obj):
        self._row_id = self._obj_db.tables[table_name].add(obj)
        self._table_name = table_name

    def revert(self):
        self._obj_db.tables[self._table_name].delete(self._row_id)
