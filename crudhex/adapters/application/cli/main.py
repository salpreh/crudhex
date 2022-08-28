from pathlib import Path
from os import sep
from typing import Optional, Tuple

import typer
from rich.console import Console
from rich.theme import Theme
from rich.progress import Progress

from crudhex.domain.models.mapper import MapperType
from crudhex.domain.models.project_config import ConfigValidationError
from crudhex.domain.services import dsl_parser, config_context, db_adapter_generator, domain_generator, rest_generator


_SPEC_HELP = 'Spec file path to process'
_CONF_HELP = f'Project config file to know packages and code paths. Defaults to {config_context.DEFAULT_CONFIG}'
_FORCE_HELP = f'Override file outputs if exists'
_MAPPER_HELP = f'Mapper generation option. By default no mapper will be generated.' \
               '\n[WARN]: modelmapper generation not supported yet.'

app = typer.Typer()
out_console: Optional[Console] = None
err_console: Optional[Console] = None


def main():
    _setup()
    app()


@app.command()
def generate(
        spec_file: str = typer.Argument(..., help=_SPEC_HELP),
        project_config: str = typer.Option(None, '--config', '-c', help=_CONF_HELP),
        force_override: bool = typer.Option(False, '--force', '-f', help=_FORCE_HELP),
        mapper_type: MapperType = typer.Option(MapperType.NONE.value, '--mapper', '-m', help=_MAPPER_HELP)
):

    load_config(project_config)
    _validate_mapper(mapper_type)

    spec_path = Path(spec_file)
    if not spec_path.exists():
        err_console.print('Unable to find spec file: {}'.format(spec_path.resolve()))
        raise typer.Exit(code=1)

    if not force_override:
        out_console.print('Force flag not enabled, existing files won\'t be generated', style='warning')

    out_console.print('Processing spec...', end='\n\n', style='notify')
    with Progress(transient=True) as progress:
        parse_task = progress.add_task('Parsing config', total=100)
        entities = dsl_parser.parse_spec_file(spec_path)
        entities_map = {e.name: e for e in entities}
        progress.update(parse_task, advance=100)

        generate_task = progress.add_task('Generate classes', total=100)

        # Shared classes
        progress.console.rule('Shared classes', style='bright_yellow')
        if mapper_type != MapperType.NONE:
            out_path = db_adapter_generator.create_mapper_class(entities_map, mapper_type, force_override)
            _log_db_adapter_generation('DB mapper', out_path, progress)

        progress.console.print('')

        # Per entity classes
        for entity in entities:
            progress.console.rule(entity.name)
            out_path = domain_generator.create_model_class(entity, force_override)
            _log_domain_generation('Domain model', out_path, progress)

            out_path = domain_generator.create_command_class(entity, entities_map, force_override)
            _log_domain_generation('Domain command', out_path, progress)

            out_path = domain_generator.create_db_port_class(entity, force_override)
            _log_domain_generation('DB port', out_path, progress)

            out_path = domain_generator.create_use_case_port_class(entity, force_override)
            _log_domain_generation('Use case port', out_path, progress)

            out_path = domain_generator.create_use_case_class(entity, force_override)
            _log_domain_generation('Use case', out_path, progress)

            out_path = db_adapter_generator.create_entity_class(entity, force_override)
            _log_db_adapter_generation('Entity', out_path, progress)

            out_path = db_adapter_generator.create_repository_class(entity, force_override)
            _log_db_adapter_generation('Repository', out_path, progress)

            out_path = db_adapter_generator.create_adapter_class(entity, entities_map, force_override)
            _log_db_adapter_generation('DB adapter', out_path, progress)

            out_path = rest_generator.create_model_class(entity, force_override)
            _log_rest_adapter_generation('Controller', out_path, progress)

            progress.update(generate_task, advance=100/len(entities))
            progress.console.print('')

        progress.update(generate_task, advance=100)

    out_console.print('\n-- All classes generated --\n', style='finished')


def load_config(project_config: Optional[str]):
    """
    Loads config file. If config cannot be loaded or invalid will raise an exeption
    :param project_config: Config path. If `None` default path will be used
    :raises Exit
    """
    if not project_config:
        out_console.print('Loading from default config path...', style='info')

    try:
        config_context.load_config(Path(project_config) if project_config else None)
        config_context.get_config().validate()
    except ConfigValidationError as err:
        err_console.print('Errors in config file: {}'.format('\n- '.join(err.errors)))
        raise typer.Exit(code=1)


def _log_domain_generation(file_type: str, gen_output: Tuple[bool, Path], progress: Optional[Progress] = None):
    _log_generation(file_type, gen_output, 'bright_blue', progress)


def _log_db_adapter_generation(file_type: str, gen_output: Tuple[bool, Path], progress: Optional[Progress] = None):
    _log_generation(file_type, gen_output, 'bright_cyan', progress)


def _log_rest_adapter_generation(file_type: str, gen_output: Tuple[bool, Path], progress: Optional[Progress] = None):
    _log_generation(file_type, gen_output, 'bright_yellow', progress)


def _log_generation(file_type: str, gen_output: Tuple[bool, Path], style: str, progress: Optional[Progress] = None):
    console = out_console
    if progress:
        console = progress.console

    if gen_output[0]:
        console.print(f'{file_type}: [default]{gen_output[1].parent}{sep}[/default][{style}]{gen_output[1].name}[/{style}]', style=style)
    else:
        console.print(f'{file_type}: [yellow]Skipped[/yellow]', style=style)


def _validate_mapper(mapper_type: MapperType):
    if mapper_type == MapperType.MODELMAPPER:
        out_console.print(f"'{mapper_type.value}' mapper type not supported yet :(", style='critical')
        raise typer.Exit(code=1)


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
