from typing import Optional

import inflect

_ENGINE: Optional[inflect.engine] = None


def get_inflect_engine():
    global _ENGINE
    if _ENGINE: return _ENGINE

    _ENGINE = inflect.engine()

    return _ENGINE
