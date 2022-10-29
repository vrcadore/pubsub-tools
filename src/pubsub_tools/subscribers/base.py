from concurrent.futures import TimeoutError
from typing import Callable

import click
from google.api_core.exceptions import AlreadyExists
from google.cloud import pubsub_v1
from google.cloud.pubsub_v1.subscriber.message import Message


def receive_messages(
    project_id: str,
    subscription_id: str,
    message_handler: Callable[[Message], None],
    timeout: int = None,
    create_sub: bool = True,
    topic_id: str = None,
) -> None:
    """Receive messages from a subscription and run a message handler for each one.

    Args:
        project_id (str): GCP project id.
        subscription_id (str): Subscription id that will attach on it.
        message_handler (Callable[[Message], None]): Custom message handler.
        timeout (int, optional): Time to run. It will run indefitively when equal None.
            Defaults to None.
        create_sub (bool, optional): Create a subscription in case it does not exists.
            Defaults to False.
        topic_id (str, optional): Topic that should be will use to create the
            subscription. Defaults to None.
    """

    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(project_id, subscription_id)

    if create_sub:
        if not topic_id:
            click.secho("Topic id not defined... skipping sub creation.", fg="red")
        else:
            try:
                click.secho("Creating a new subscription.\n", fg="green")
                publisher = pubsub_v1.PublisherClient()
                topic_path = publisher.topic_path(project_id, topic_id)
                subscription = subscriber.create_subscription(
                    name=subscription_path, topic=topic_path
                )
                click.secho(
                    f"The subscription created: {subscription.name}\n", fg="green"
                )
            except AlreadyExists as e:
                click.secho(
                    f"The subscription already exists, detail: {str(e)}\n", fg="yellow"
                )
                # Ignore the error, fetch the topic

    def callback(message: Message) -> None:
        click.secho(f"\nReceived {message}.", fg="cyan")
        message.ack()

    if not message_handler:
        message_handler = callback

    streaming_pull_future = subscriber.subscribe(
        subscription_path, callback=message_handler
    )
    click.secho(
        f"Listening for messages on {subscription_path}..\n", fg="green", bold=True
    )

    # Wrap subscriber in a 'with' block to automatically call close() when done.
    with subscriber:
        try:
            # When `timeout` is not set, result() will block indefinitely,
            # unless an exception is encountered first.
            streaming_pull_future.result(timeout=timeout)
        except TimeoutError:
            click.secho("\nTimeout reached...\n", fg="red", bold=True)
            streaming_pull_future.cancel()  # Trigger the shutdown.
            streaming_pull_future.result()  # Block until the shutdown is complete.
