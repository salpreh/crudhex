import typer


def mutually_exclusive_group(size=1):
    """
    Extracted from https://github.com/tiangolo/typer/issues/140#issuecomment-898937671
    """
    group = set()

    def callback(ctx: typer.Context, param: typer.CallbackParam, value: str):
        # Add cli option to group if it was called with a value
        if value and param.name not in group:
            group.add(param.name)
        if len(group) > size:
            raise typer.BadParameter(f"{param.name} is mutually exclusive with {group.pop()}")

        return value

    return callback
