import click

from pubsub_tools.publishers.base import generate_messages
from pubsub_tools.publishers.generators.csv_sample import get_csv_sample
from pubsub_tools.publishers.generators.wiki import get_random_summaries

SAMPLE = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"


# Command Group
@click.group(name="pub")
@click.pass_context
def pub_group(ctx: click.Context) -> None:
    """Publisher helper commands.

    Args:
        ctx (click.Context): Command context.
    """
    pass


@pub_group.command()
@click.option("--topic-id", required=True, help="Input PubSub topic id.")
@click.option("--num-iterations", default=25, help="Number of records.")
@click.option("--dry-run", is_flag=True, help="Disable sending messages to pub/sub.")
@click.option("--create-topic", is_flag=True, help="Create topic.")
@click.pass_context
def wiki(
    ctx: click.Context,
    topic_id: str,
    num_iterations: int,
    dry_run: bool,
    create_topic: bool,
) -> None:
    """Run Random Wiki publisher.

    Args:
        ctx (click.Context): Command context.
        topic_id (str): Pub/Sub topic id.
        num_iterations (int): Number of records.
        dry_run (bool): Disable sending messages to pub/sub.
    """

    project_id = ctx.obj["PROJECT-ID"]

    click.secho(
        "\nGenerate random wiki article messages in Pub/Sub.\n", fg="cyan", bold=True
    )
    if dry_run:
        click.secho("* Dry-run mode activated.", fg="yellow", bold=True)
    click.secho(f"* Topic: {topic_id}", fg="white")
    click.secho(f"* Number of Messages:{num_iterations}\n", fg="white")

    generator = get_random_summaries(num_iterations=num_iterations)
    generate_messages(
        project_id, topic_id, generator, dry_run=dry_run, create_topic=create_topic
    )


@pub_group.command(name="csv-sample")
@click.option("--topic-id", required=True, help="Pub/Sub topic id.")
@click.option(
    "--file",
    default=SAMPLE,
    help="CSV File that we will use to sample data.",
)
@click.option("--msg-format", default="csv", help="Format of result message[dict|csv].")
@click.option("--num-iterations", default=25, help="Number of records.")
@click.option("--sleep-ms", default=100, help="Time to wait after each message(ms).")
@click.option("--dry-run", is_flag=True, help="Disable sending messages to pub/sub.")
@click.option("--create-topic", is_flag=True, help="Create topic.")
@click.pass_context
def csv_sample(
    ctx: click.Context,
    topic_id: str,
    file: str,
    msg_format: str,
    num_iterations: int,
    sleep_ms: int,
    dry_run: bool,
    create_topic: bool,
) -> None:
    """Generate messages sampling data from a CSV.

    Args:
        ctx (click.Context): Command context.
        topic_id (str): Pub/Sub topic id.
        file (str): CSV File that we will use to sample data.
        msg_format (str): Format of result message[dict|csv].
        num_iterations (int): Number of records.
        sleep_ms (int): Time to wait after each message(ms).
        dry_run (bool): Disable sending messages to pub/sub.
        create_topic (bool, optional): Create topic. Defaults to False.
    """

    project_id = ctx.obj["PROJECT-ID"]

    click.secho(
        "\nGenerate random rows messages from a CSV in Pub/Sub.\n", fg="cyan", bold=True
    )
    if dry_run:
        click.secho("* Dry-run mode activated.", fg="yellow", bold=True)
    click.secho(f"* Topic: {topic_id}", fg="white")
    click.secho(f"* CSV File: {file}", fg="white")
    click.secho(f"* Number of Messages:{num_iterations}\n", fg="white")

    generator = get_csv_sample(
        file, num_iterations=num_iterations, msg_format=msg_format, sleep_ms=sleep_ms
    )
    generate_messages(
        project_id, topic_id, generator, dry_run=dry_run, create_topic=create_topic
    )


if __name__ == "__main__":
    pub_group()
