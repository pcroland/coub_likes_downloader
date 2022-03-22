#!/usr/bin/env python3
import http.cookiejar
import subprocess
import argparse
import requests
from rich import print
from rich.progress import track
import sys


parser = argparse.ArgumentParser(
    add_help=False, formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, max_help_position=40)
)
parser.add_argument('-h', '--help',
                    action='help',
                    default=argparse.SUPPRESS,
                    help='shows this help message.')
parser.add_argument('-v', '--version',
                    action='version',
                    version='coub.py 1.1.0',
                    help='shows version.')
parser.add_argument('-l', '--liked',
                    action='store_true',
                    help='download liked coubs')
parser.add_argument('-u', '--user',
                    type=str,
                    default='',
                    help='specify user')
parser.add_argument('-f', '--force-remux',
                    action='store_true',
                    help='forcing remux to mp4, requires ffmpeg')
args = parser.parse_args()

def main():
    if not args.liked and not args.user:
        print('[red]ERROR: you have to use the -l or -u option, see [bold]--help[/bold].[/red]')
        sys.exit(1)

    if args.liked:
        search = 'likes'
    elif args.user:
        search = f'channel/{args.user}'

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
        if args.force_remux:
            yt_dlp_args = ['yt-dlp', '-o', f'%(upload_date)s_%(title)s_[%(uploader)s] [%(id)s].%(ext)s', f'https://coub.com/view/{url}']
        else:
            yt_dlp_args = ['yt-dlp', '--remux-video', 'mp4', '-o', f'%(upload_date)s_%(title)s_[%(uploader)s] [%(id)s].%(ext)s', f'https://coub.com/view/{url}']
        subprocess.run(yt_dlp_args, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)


if __name__ == '__main__':
    main()
