import click


# Command Group
@click.group(name="utils")
def utils_group(ctx: click.Context) -> None:
    """Utils commands."""
    pass


@utils_group.command()
def create_topic(ctx: click.Context) -> None:
    """Meh."""
    pass


@utils_group.command()
def create_sub(ctx: click.Context) -> None:
    """Meh."""
    pass


if __name__ == "__main__":
    utils_group()
