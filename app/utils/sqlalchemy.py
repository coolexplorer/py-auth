from sqlalchemy import inspect
from typing import Dict

def object_as_dict(obj) -> Dict:
    return {c.key: getattr(obj, c.key)
            for c in inspect(obj).mapper.column_attrs}
