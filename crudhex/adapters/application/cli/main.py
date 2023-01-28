from typing import Optional

import typer
from rich.console import Console
from rich.theme import Theme

from . import console_out_context as console_context
from .commands.generate_crud import generate as generate_crud
from .commands import create_project
from crudhex.domain.models.mapper import MapperType
from crudhex.domain.services import project_config_context

_SPEC_HELP = 'Spec file path to process'
_CONF_HELP = f'Project config file to know packages and code paths. Defaults to {project_config_context.DEFAULT_CONFIG}'
_FORCE_HELP = f'Override file outputs if exists'
_MAPPER_HELP = f'Mapper generation option. By default no mapper will be generated.' \
               '\n[WARN]: modelmapper generation not supported yet.'
_API_MODELS_HELP = 'Generate API models'
_API_PAGE_HELP = 'Use Spring data Page as return type for get all endpoints. By default List with items is returned'
_EXCEPTION_HANDLER_HELP = 'Generate a default exception handler for Spring REST controllers (ControllerAdvice)'

app = typer.Typer()
out_console: Optional[Console] = None
err_console: Optional[Console] = None


def main():
    _setup()
    _load_subcommands()
    app()


@app.command(help='Generate CRUD classes from a spec file', name='crud')
def generate_crud(
        spec_file: str = typer.Argument(..., help=_SPEC_HELP),
        project_config: str = typer.Option(None, '--config', '-c', help=_CONF_HELP),
        force_override: bool = typer.Option(False, '--force', '-f', help=_FORCE_HELP),
        mapper_type: MapperType = typer.Option(MapperType.NONE.value, '--mapper', '-m', help=_MAPPER_HELP),
        gen_api_models: bool = typer.Option(True, '--generate-api-models/--no-generate-api-models', help=_API_MODELS_HELP),
        with_api_page: bool = typer.Option(False, '--with-api-page', '-ap', help=_API_PAGE_HELP),
        add_exception_handler: bool = typer.Option(True, '--add-exception-handler/--no-add-exception-handler', help=_EXCEPTION_HANDLER_HELP)
):

    generate_crud(spec_file, project_config, force_override,
                  mapper_type, gen_api_models, with_api_page,
                  add_exception_handler)


def _load_subcommands():
    try:
        import cookiecutter

        app.add_typer(create_project.app, name='project', help='Create a new project from template')
    except ImportError:
        pass


def _setup():
    theme = Theme({
        "light": "gray74",
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
