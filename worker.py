from google.cloud import pubsub
import subprocess as sp

subscriber = pubsub.SubscriberClient()
subscription = subscriber.subscribe(
    'projects/visualdb-1046/subscriptions/queue_example_sub')
    
def download_video(id):
    sp.check_call(
        'youtube-dl -f mp4 "http://youtube.com/watch?v={id}" -o {id}.mp4 --no-cache-dir'
        .format(id=id),
        shell=True)

def copy_to_gcs(id):
    sp.check_call(
        'gsutil mv {id}.mp4 gs://esper/tmp/videos/'.format(id=id),
        shell=True)

def callback(message):
    id = message.data
    download_video(id)
    copy_to_gcs(id)
    message.ack()

subscription.open(callback).result()

    
