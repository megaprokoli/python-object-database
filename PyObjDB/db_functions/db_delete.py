from PyObjDB.db_functions.db_function import DatabaseFunction


class DBDelete(DatabaseFunction):
    def __init__(self, obj_db):
        super().__init__(obj_db)
        self._table_name = None
        self._old_objs = None
        self._key = None

    def call(self, table_name, key=None, filter_func=None):
        self._table_name = table_name
        self._old_objs = self._obj_db.get(table_name, key, filter_func)
        self._key = key

        self._obj_db.tables[table_name].delete(key, filter_func)

    def revert(self):
        for key, obj in self._old_objs.items():
            self._obj_db.tables[self._table_name].set(key, obj)
