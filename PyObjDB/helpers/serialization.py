import dill
import base64


def serialize(obj):
    ser = dill.dumps(obj)
    return base64.b64encode(ser).decode("utf-8")


def deserialize(obj_str):
    decoded = base64.b64decode(obj_str)
    return dill.loads(decoded)
