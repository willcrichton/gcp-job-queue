from google.cloud import pubsub
from google.cloud import monitoring
import time

PROJECT = 'wc-personal'
TOPIC = 'queue-example'
SUBSCRIPTION = 'queue-example-sub'


# This is a dirty hack since Pub/Sub doesn't expose a method for determining
# if the queue is empty (to my knowledge). We have to use the metrics API which
# is only updated every minute. Hopefully someone from Google can clarify!
def queue_empty(client):
    result = client.query(
        'pubsub.googleapis.com/subscription/num_undelivered_messages',
        minutes=1).as_dataframe()
    return result['pubsub_subscription'][PROJECT][SUBSCRIPTION][0] == 0


def print_message(message):
    print(message.data)
    message.ack()


def main():
    client = monitoring.Client(project=PROJECT)

    # Publishes the message 'Hello World'
    publisher = pubsub.PublisherClient()
    topic = 'projects/{}/topics/{}'.format(PROJECT, TOPIC)
    publisher.publish(topic, 'Hello world!')

    # Opens a connection to the message queue asynchronously
    subscriber = pubsub.SubscriberClient()
    subscription = subscriber.subscribe('projects/{}/subscriptions/{}'.format(
        PROJECT, SUBSCRIPTION))
    subscription.open(print_message)

    # Waits until the queue is empty to exit. See queue_empty for more
    # explanation.
    time.sleep(60)
    while not queue_empty(client):
        pass
    subscription.close()


if __name__ == '__main__':
    main()
