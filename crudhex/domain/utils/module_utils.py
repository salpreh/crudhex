from inspect import getmembers, isfunction
from types import ModuleType


def extract_functions(module: ModuleType, scope: dict):
    for name, func in getmembers(module, isfunction):
        scope[name] = func
