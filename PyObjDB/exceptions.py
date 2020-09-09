class ObjectMismatch(ValueError):
    pass


class TableDoesNotExist(KeyError):
    pass


class TableAlreadyExists(ValueError):
    pass


class EntryExists(ValueError):
    pass
