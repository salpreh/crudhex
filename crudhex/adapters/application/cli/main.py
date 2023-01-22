from typing import Optional

import typer
from rich.console import Console
from rich.theme import Theme

from . import console_out_context as console_context
from .commands import generate_crud

app = typer.Typer()
out_console: Optional[Console] = None
err_console: Optional[Console] = None


def main():
    _setup()
    _enable_commands()
    app()


def _enable_commands():
    app.add_typer(generate_crud.app, name='generate', help='Generate CRUD classes from a spec file')


def _setup():
    theme = Theme({
        "notify": "cyan",
        "info": "dim cyan",
        "success": "green",
        "finished": "black on green",
        "warning": "yellow",
        "error": "red",
        "critical": "bold red"
    })

    global out_console
    out_console = Console(theme=theme)

    global err_console
    err_console = Console(stderr=True, style="red")

    console_context.set_out_consoles(out_console, err_console)
