from typing import Optional

import typer
from cookiecutter.main import cookiecutter
from rich.console import Console

from .. import console_out_context as console_context
from ..cli_helper import mutually_exclusive_group

_CREATE_HELP = 'Create a new project scaffolding'
_LIST_HELP = 'List available templates'

_TEMPLATE_NAME_HELP = 'Name of the template to use. Exclusive options: -t, -f, -g'
_TEMPLATE_FOLDER_HELP = 'Folder where the template is located. Exclusive options: -t, -f, -g'
_TEMPLATE_GIT_HELP = 'Git repository where the template is located. Exclusive options: -t, -f, -g'

app = typer.Typer()
out_console: Optional[Console] = None
err_console: Optional[Console] = None

template_group_callback = mutually_exclusive_group()


@app.command(help=_CREATE_HELP)
def create(
        template_name: str = typer.Option(None, '--template-name', '-t', help=_TEMPLATE_NAME_HELP, callback=template_group_callback),
        template_folder: str = typer.Option(None, '--template-folder', '-f', help=_TEMPLATE_FOLDER_HELP, callback=template_group_callback),
        template_git: str = typer.Option(None, '--template-git', '-g', help=_TEMPLATE_GIT_HELP, callback=template_group_callback),
        output_dir: str = typer.Option('.', '--output-dir', '-o', help='Output directory for the generated project')
):
    _set_up()

    if template_name:
        out_console.print(f'Using template {template_name}', style='info')
        template_ref = _get_template_ref(template_name)
    else:
        template_ref = template_folder or template_git

    out_console.print(f'Creating project template\n', style='notify')

    cookiecutter(template_ref, output_dir=output_dir)

    out_console.print(f'\nTemplate generated!', style='finished')


@app.command(name='list', help=_LIST_HELP)
def list_available():
    out_console.print(f'Template list!', style='finished')


def _get_template_ref(template_name: str) -> str:
    out_console.print(f'Template {template_name} not found!', style='error')
    raise typer.Exit(code=1)


def _set_up():
    global out_console, err_console
    out_console = console_context.get_out_console()
    err_console = console_context.get_err_console()
