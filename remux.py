#!/usr/bin/env python3

from glob import glob
import os
import subprocess
from time import sleep
from rich.progress import track
from sys import exit

MAX_VIDEO_LENGHT = "30" #seconds
success = 0
total = 0
try:
    os.mkdir('final')
except FileExistsError:
    pass
except Exception as e:
    print(e)
    exit(1)

for video in track(glob('*high*.mp4'), description='Remux'):
    total += 1
    basename = video.split(sep='-video')
    audio = basename[0] + '-audio-high.mp3'
    final = 'final/' + basename[0] + '-final.mp4'
    if not os.path.exists(audio):
        print(f"No mp3 file found for: {video}")
    else:
        ff_args = ['ffmpeg', '-stream_loop', '-1', '-i', video, '-i', audio,
                    '-shortest', '-map', '0:v:0', '-map', '1:a:0', 
                    '-c:v', 'copy', '-c:a', 'copy',
                    '-t', MAX_VIDEO_LENGHT,
                    '-y', final]

        print(f"File: {final}")
        res = subprocess.run(ff_args, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
        if res.returncode != 0:
            print(f"ERROR: Could not remuxed video file: {video}")
        else:
            success += 1

print(f"Success: {success}/{total}")