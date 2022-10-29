import click

from pubsub_tools.subscribers.base import receive_messages


# Command Group
@click.group(name="sub")
@click.pass_context
def sub_group(ctx: click.Context) -> None:
    """Subscriber helper commands."""
    pass


@sub_group.command()
@click.option("--subscription-id", required=True, help="Input PubSub subscriber id.")
@click.option("--timeout", type=int, help="Time to run the command.")
@click.option(
    "--create-sub",
    is_flag=True,
    help="Create a subscription in case it does not exists. ",
)
@click.option("--topic-id", help="Pub/Sub topic id.")
@click.pass_context
def simple_sub(
    ctx: click.Context,
    subscription_id: str,
    timeout: int = None,
    create_sub: bool = True,
    topic_id: str = None,
) -> None:
    """Run Simple Message Subscriber."""

    project_id = ctx.obj["PROJECT-ID"]

    click.secho("\nRead messages from a subscriber in Pub/Sub.\n", fg="cyan", bold=True)
    click.secho(f"* Subscription: {subscription_id}", fg="white")
    if topic_id:
        click.secho(f"* Topic: {topic_id}", fg="white")
    click.secho(f"* Timeout: {timeout}\n", fg="white")

    receive_messages(
        project_id=project_id,
        subscription_id=subscription_id,
        message_handler=None,
        timeout=timeout,
        create_sub=create_sub,
        topic_id=topic_id,
    )


if __name__ == "__main__":
    sub_group()
