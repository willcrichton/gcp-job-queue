from google.cloud import pubsub
from tqdm import tqdm

with open('youtube-ids') as f:
    ids = [s.strip() for s in f.readlines()]

publisher = pubsub.PublisherClient()
topic = 'projects/visualdb-1046/topics/queue-example'
for id in tqdm(ids):
    publisher.publish(topic, id)
