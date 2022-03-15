#!/usr/bin/env python3
import http.cookiejar
import subprocess

import requests
from rich import print
from rich.progress import track
import sys

if len(sys.argv) == 2:
    search = f'channel/{sys.argv[1]}'
else:
    search = 'likes'
session = requests.Session()
session.cookies = http.cookiejar.MozillaCookieJar('cookies.txt')
session.cookies.load()

print(f'[color(231)]Fetching number of pages of[/color(231)] [magenta]api/v2/timeline/[bold]{search}[/bold][/magenta]: ', end='')
a = session.get(f'https://coub.com/api/v2/timeline/{search}?page=1&per_page=25').json()
pages = a['total_pages']
print(f'[bold cyan]{pages}[/bold cyan]')

url_list = []
for page in track(range(1, pages + 1), description='[color(231)]Grabbing links... [/color(231)]'):
    page = session.get(f'https://coub.com/api/v2/timeline/{search}?page={page}&per_page=25').json()
    coubs = page['coubs']
    for coub in coubs:
        url_list.append(coub['permalink'])
print(f'[color(231)]Number of coubs:[/color(231)] [bold cyan]{len(url_list)}[/bold cyan]')

for url in track(url_list, description='[color(231)]Grabbing videos...[/color(231)]'):
    yt_dlp_args = ['yt-dlp', '-o', f'%(upload_date)s_%(title)s_[%(uploader)s] [%(id)s].%(ext)s', f'https://coub.com/view/{url}']
    subprocess.run(yt_dlp_args, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
