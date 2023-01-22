from typing import Optional

import typer
from rich.console import Console

from .. import console_out_context as console_context

app = typer.Typer()
out_console: Optional[Console] = None
err_console: Optional[Console] = None


@app.command(help='Create a new project scaffolding')
def create(
        template_name: str = typer.Argument(..., help="Name of the template to use")
):
    _set_up()
    out_console.print(f'Creating template {template_name}')
    out_console.print(f'Template generated!', style='finished')


@app.command(name='list', help='List available templates')
def list_available():
    out_console.print(f'Template list!', style='finished')


def _set_up():
    global out_console, err_console
    out_console = console_context.get_out_console()
    err_console = console_context.get_err_console()
