from google.cloud import pubsub
from google.cloud import monitoring
import subprocess as sp
import time

PROJECT = 'wc-personal'
TOPIC = 'queue-example'
SUBSCRIPTION = 'queue-example-sub'
BUCKET = 'wc-personal-test'


def queue_empty(client):
    result = client.query(
        'pubsub.googleapis.com/subscription/num_undelivered_messages',
        minutes=1).as_dataframe()
    return result['pubsub_subscription'][PROJECT][SUBSCRIPTION][0] == 0


def download_video(id):
    sp.check_call(
        'youtube-dl -f mp4 "http://youtube.com/watch?v={id}" -o {id}.mp4 --no-cache-dir'
        .format(id=id),
        shell=True)


def copy_to_gcs(id):
    sp.check_call('gsutil mv {}.mp4 gs://{}/tmp/videos/'.format(id, BUCKET), shell=True)


def handle_message(message):
    id = message.data
    download_video(id)
    # copy_to_gcs(id)
    message.ack()


def main():
    client = monitoring.Client(project=PROJECT)

    subscriber = pubsub.SubscriberClient()
    subscription = subscriber.subscribe('projects/{}/subscriptions/{}'.format(
        PROJECT, SUBSCRIPTION))
    subscription.open(handle_message)

    time.sleep(60)
    while not queue_empty(client):
        pass
    subscription.close()


if __name__ == '__main__':
    main()
