class DBEntry:
    def __init__(self, key: str, obj: object):
        self.key = key
        self.obj = obj

    def __str__(self):
        return f"{self.key}: {self.obj}"
