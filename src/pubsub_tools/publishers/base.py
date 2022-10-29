from typing import Generator

import click
from google.api_core.exceptions import AlreadyExists
from google.cloud import pubsub_v1


def generate_messages(
    project_id: str,
    topic_id: str,
    generator: Generator[str, None, None],
    dry_run: bool = False,
    create_topic: bool = False,
) -> None:
    """Reads message from a generator and public to Pub/Sub

    Args:
        project_id (str): Pub/Sub project id.
        topic_id (str): Pub/Sub topic id.
        generator (Generator[str, None, None]): Message generator.
        dry_run (bool, optional): Defines if it is a dry-run. Defaults to False.
        create_topic (bool, optional): Create topic. Defaults to False.
    """
    if not dry_run:
        publisher = pubsub_v1.PublisherClient()
        topic_path = publisher.topic_path(project_id, topic_id)
        click.secho(f"Publishing messages to {topic_path}.", fg="yellow")

        try:
            if create_topic:
                click.secho("Creating a new topic.", fg="green")
                topic = publisher.create_topic(name=topic_path)
                click.secho(f"The topic created: {topic.name}", fg="green")
        except AlreadyExists as e:
            click.secho(f"The topic already exists, detail: {str(e)}", fg="yellow")
            # Ignore the error, fetch the topic

    def get_callback(f, data):
        def callback(f):
            try:
                id = f.result()
                abbv_data = data
                if len(abbv_data) > 50:
                    abbv_data = abbv_data[:50] + b"..."
                click.secho(
                    f"Sent Message {{\n  id: {id}\n  data: {abbv_data}\n}}\n",
                    fg="magenta",
                )
            except:  # noqa
                print(
                    "Error sending... Exception {} for {}.".format(f.exception(), data)
                )

        return callback

    for msg in generator:
        # Data must be a bytestring
        data = msg.encode("utf-8")

        # When you publish a message, the client returns a future.
        if not dry_run:
            future = publisher.publish(topic_path, data)
            future.add_done_callback(get_callback(future, data))
