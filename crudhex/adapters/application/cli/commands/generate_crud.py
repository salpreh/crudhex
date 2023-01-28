from pathlib import Path
from os import sep
from typing import Optional, Tuple, Dict

import typer
from rich.console import Console
from rich.progress import Progress

from crudhex.adapters.application.cli import console_out_context as console_context
from crudhex.domain.models import Entity
from crudhex.domain.models.mapper import MapperType
from crudhex.domain.models.project_config import ConfigValidationError
from crudhex.domain.services import dsl_parser, project_config_context, db_adapter_generator, domain_generator, rest_generator

out_console: Optional[Console] = None
err_console: Optional[Console] = None


def generate(
        spec_file: str,
        project_config: str,
        force_override: bool,
        mapper_type: MapperType,
        gen_api_models: bool,
        with_api_page: bool,
        add_exception_handler: bool
):

    _set_up()
    _load_config(project_config)
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
        out_path = domain_generator.create_not_found_exception_class(force_override)
        _log_domain_generation('Not found exception', out_path, progress)

        if mapper_type != MapperType.NONE:
            out_path = db_adapter_generator.create_mapper_class(entities_map, mapper_type, force_override)
            _log_db_adapter_generation('DB mapper', out_path, progress)

            if gen_api_models:
                out_path = rest_generator.create_mapper_class(entities_map, mapper_type, force_override)
                _log_rest_adapter_generation('API mapper', out_path, progress)

        if add_exception_handler:
            out_path = rest_generator.create_exception_handler_class(force_override)
            _log_rest_adapter_generation('Exception handler', out_path, progress)

        progress.console.print('')

        # Per entity classes
        for entity in entities:
            progress.console.rule(entity.name)
            _generate_domain_classes(entity, entities_map, progress, force_override)
            _generate_db_classes(entity, entities_map, progress, force_override)
            _generate_rest_classes(entity, entities_map, progress, force_override, gen_api_models, with_api_page)

            progress.update(generate_task, advance=100/len(entities))
            progress.console.print('')

        progress.update(generate_task, advance=100)

    out_console.print('\n-- All classes generated --\n', style='finished')


def _load_config(project_config: Optional[str]):
    """
    Loads config file. If config cannot be loaded or invalid will raise an exception
    :param project_config: Config path. If `None` default path will be used
    :raises Exit
    """
    if not project_config:
        out_console.print('Loading from default config path...', style='info')

    try:
        project_config_context.load_project_config(Path(project_config) if project_config else None)
        project_config_context.get_project_config().validate()
    except ConfigValidationError as err:
        err_console.print('Errors in config file: {}'.format('\n- '.join(err.errors)))
        raise typer.Exit(code=1)


def _set_up():
    global out_console, err_console
    out_console = console_context.get_out_console()
    err_console = console_context.get_err_console()


def _generate_domain_classes(entity: Entity, entities_map: Dict[str, Entity], progress: Progress, force_override: bool):
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


def _generate_db_classes(entity: Entity, entities_map: Dict[str, Entity], progress: Progress, force_override: bool):
    out_path = db_adapter_generator.create_entity_class(entity, force_override)
    _log_db_adapter_generation('Entity', out_path, progress)

    out_path = db_adapter_generator.create_repository_class(entity, force_override)
    _log_db_adapter_generation('Repository', out_path, progress)

    out_path = db_adapter_generator.create_adapter_class(entity, entities_map, force_override)
    _log_db_adapter_generation('DB adapter', out_path, progress)


def _generate_rest_classes(entity: Entity, entities_map: Dict[str, Entity], progress: Progress,
                           force_override: bool, gen_api_models: bool, with_api_page: bool):
    out_path = rest_generator.create_controller_class(entity, force_override, gen_api_models, with_api_page)
    _log_rest_adapter_generation('Controller', out_path, progress)

    if gen_api_models:
        out_path = rest_generator.create_model_class(entity, force_override)
        _log_rest_adapter_generation('Model', out_path, progress)


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
