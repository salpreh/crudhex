from typing import Optional
from shutil import rmtree

import typer
from rich.console import Console

from .. import console_out_context as console_context
from ..cli_helper import mutually_exclusive_group
from crudhex.domain.services.config_context import get_project_config

# Optional imports. cookiecutter should be checked before using this module
try:
    from cookiecutter.main import cookiecutter
    from cookiecutter import repository
    from cookiecutter.config import get_user_config as get_cookiecutter_config
except ImportError:
    cookiecutter = None
    repository = None
    get_cookiecutter_config = None

_CREATE_HELP = 'Create a new project scaffolding'
_LIST_HELP = 'List available templates'

_TEMPLATE_NAME_HELP = 'Name of the template to use. Exclusive options: -t, -f, -g'
_TEMPLATE_FOLDER_HELP = 'Folder where the template is located. Exclusive options: -t, -f, -g'
_TEMPLATE_GIT_HELP = 'Git repository where the template is located. Exclusive options: -t, -f, -g'
_LIST_ALL_HELP = 'List templates with source information'

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
        template_ref = _get_template_ref(template_name)
        cleanup = repository.is_repo_url(template_ref)
    elif template_folder:
        template_ref = template_folder
        cleanup = False
    else:
        template_ref = template_git
        cleanup = True

    out_console.print(f'Creating project template\n', style='notify')

    cookiecutter(template_ref, output_dir=output_dir)

    if cleanup:
        out_console.print(f'\nCleaning up temp files', style='info')
        _cleanup_template(template_ref)

    out_console.print(f'\n-- Template generated! --\n', style='finished')


@app.command(name='list', help=_LIST_HELP)
def list_available(
        full_output: bool = typer.Option(False, '--all', '-a', help=_LIST_ALL_HELP)
):
    _set_up()
    out_console.print(f'Listing configured templates:', style='notify')
    config = get_project_config()
    if not config.templates:
        out_console.print(f'No templates configured', style='warning')
        typer.Exit(code=0)

    for template, ref in config.templates.items():
        if full_output:
            out_console.print(f' - [bold]{template}[/bold]: [light]{ref}[/light]')
        else:
            out_console.print(f' - {template}')


def _get_template_ref(template_name: str) -> str:
    config = get_project_config()
    template_ref = config.templates.get(template_name)
    if not template_ref:
        out_console.print(f'Template {template_name} not found!', style='error')
        raise typer.Exit(code=1)

    out_console.print(f'Using template ref {template_ref}', style='info')

    return template_ref


def _cleanup_template(template_ref: str):
    config = get_cookiecutter_config()
    template_dir, _ = repository.determine_repo_dir(template_ref, config['abbreviations'],
                                                    config['cookiecutters_dir'], None, True)
    if template_dir:
        out_console.print(f'Removing template dir {template_dir}', style='info')
        rmtree(template_dir)


def _set_up():
    global out_console, err_console
    out_console = console_context.get_out_console()
    err_console = console_context.get_err_console()
