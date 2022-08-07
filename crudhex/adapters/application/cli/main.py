from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.theme import Theme
from rich.progress import Progress

from crudhex.domain.services import dsl_parser, db_adapter_generator, config_context


_CONF_HELP = f'Project config file to know packages and code paths. defaults to {config_context.DEFAULT_CONFIG}'
_SPEC_HELP = 'Spec file path to process'

app = typer.Typer()
out_console: Optional[Console] = None
err_console: Optional[Console] = None


def main():
    _setup()
    app()


@app.command()
def generate(
        project_config: str = typer.Option(None, '--config', '-c', help=_CONF_HELP),
        spec_file: str = typer.Argument(..., help=_SPEC_HELP)
):
    if not project_config:
        out_console.print('Loading from default config path...', style='info')

    config_context.load_config(Path(project_config) if project_config else None)

    spec_path = Path(spec_file)
    if not spec_path.exists():
        err_console.print('Unable to find spec file: {}'.format(spec_path.resolve()))
        raise typer.Exit(code=1)

    out_console.print('Processing spec...', end='\n\n', style='notify')
    with Progress(transient=True) as progress:
        parse_task = progress.add_task('Parsing config', total=100)
        entities = dsl_parser.parse_spec_file(spec_path)
        progress.update(parse_task, advance=100)

        generate_task = progress.add_task('Generate classes', total=100)
        for entity in entities:
            entity_path = db_adapter_generator.create_entity_class(entity)
            progress.console.print(f'Generated entity: {entity_path.resolve()}', style='cyan')

            repo_path = db_adapter_generator.create_repository_class(entity)
            progress.console.print(f'Generated repository: {repo_path.resolve()}', style='cyan')

            progress.update(generate_task, advance=100/len(entities))
            progress.console.print('\n')

        progress.update(generate_task, advance=100)

    out_console.print('\nAll entities generated', style='success')


def _setup():
    theme = Theme({
        "notify": "cyan",
        "info": "dim cyan",
        "success": "green",
        "warning": "yellow",
        "error": "red",
        "critical": "bold red"
    })

    global out_console
    out_console = Console(theme=theme)

    global err_console
    err_console = Console(stderr=True, style="red")
