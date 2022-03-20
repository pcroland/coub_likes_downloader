# Installation
```
git clone https://github.com/pcroland/coub_likes_downloader
cd coub_likes_downloader
pip install -r requirements.txt
```
# Usage
- download cookies.txt and put it next to the script. (use [Get cookies.txt](https://chrome.google.com/webstore/detail/get-cookiestxt/bgaddhkoddajcdgocldbbfleckgcbcid) for example)
- run script.

### Examples
`./coub.py` (download all liked videos)\
`./coub.py xyz` (download all videos from user xyz)

![img](https://i.kek.sh/aL0HmMqxk0o.gif)

## Remuxing the separated mp3 and mp4 files

### FFmpeg
First of all, you need ffmpeg installed

### Example
`./remux.py`

This file will create `final` folder in the actual directory, and create the joined coubs under it.