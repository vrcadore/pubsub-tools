import click
import google.auth

from pubsub_tools.publishers.commands import pub_group
from pubsub_tools.subscribers.commands import sub_group
from pubsub_tools.utils.commands import utils_group


@click.group()
@click.option("--project-id", help="GCP project id.")
@click.pass_context
def main(ctx: click.Context, project_id: str):
    """Pub/Sub Data Generator and Helper Functions.

    Args:
        ctx (click.Context): Click context.
        project_id (str): GCP project it.
    """
    ctx.ensure_object(dict)
    ctx.obj["PROJECT-ID"] = project_id

    if not project_id:
        _, project_id = google.auth.default()
        ctx.obj["PROJECT-ID"] = project_id


# Add sub commands
main.add_command(pub_group)
main.add_command(sub_group)
main.add_command(utils_group)

if __name__ == "__main__":
    main()
