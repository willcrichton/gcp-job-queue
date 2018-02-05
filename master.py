from google.cloud import pubsub
from tqdm import tqdm

PROJECT = 'wc-personal'
TOPIC = 'queue-example'


def main():
    with open('youtube-ids') as f:
        ids = [s.strip() for s in f.readlines()]

    publisher = pubsub.PublisherClient()
    topic = 'projects/{}/topics/{}'.format(PROJECT, TOPIC)
    for id in tqdm(ids):
        publisher.publish(topic, id)


if __name__ == '__main__':
    main()
