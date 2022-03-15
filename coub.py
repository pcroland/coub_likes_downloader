#!/usr/bin/env python3
import http.cookiejar
import subprocess

import requests
from rich import print
from rich.progress import track

session = requests.Session()
session.cookies = http.cookiejar.MozillaCookieJar('cookies.txt')
session.cookies.load()

print('[bold cyan]Fetching number of pages... [/bold cyan]', end='')
a = session.get('https://coub.com/api/v2/timeline/likes?all=true&order_by=date&page=1&per_page=25').json()
pages = a['total_pages']
print(f'[color(231)]{pages}[/color(231)]')

url_list = []
for page in track(range(1, pages + 1), description='Grabbing links... '):
    page = session.get(f'https://coub.com/api/v2/timeline/likes?all=true&order_by=date&page={page}&per_page=25').json()
    coubs = page['coubs']
    for coub in coubs:
        url_list.append(coub['permalink'])

for url in track(url_list, description='Grabbing videos...'):
    yt_dlp_args = ['yt-dlp', '-o', f'%(upload_date)s_%(title)s_[%(uploader)s] [%(id)s].%(ext)s', f'https://coub.com/view/{url}']
    subprocess.run(yt_dlp_args, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
