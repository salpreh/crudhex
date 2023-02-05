from typing import Tuple

from rich.console import Console

_OUT_CONSOLE = Console()
_ERR_CONSOLE = Console(stderr=True)


def get_out_console() -> Console:
    return _OUT_CONSOLE


def get_err_console() -> Console:
    return _ERR_CONSOLE


def get_out_consoles() -> Tuple[Console, Console]:
    """
    Returns a tuple with output and error consoles
    """
    return _OUT_CONSOLE, _ERR_CONSOLE


def set_out_consoles(out_console: Console, err_console: Console):
    set_out_console(out_console)
    set_err_console(err_console)


def set_out_console(console: Console):
    global _OUT_CONSOLE
    _OUT_CONSOLE = console


def set_err_console(console: Console):
    global _ERR_CONSOLE
    _ERR_CONSOLE = console
