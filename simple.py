import subprocess as sp

def download_video(id):
    sp.check_call(
        'youtube-dl -f mp4 "http://youtube.com/watch?v={id}" -o {id}.mp4'
        .format(id=id),
        shell=True)

with open('youtube-ids') as f:
    ids = [s.strip() for s in f.readlines()]

for id in ids:
    download_video(id)

