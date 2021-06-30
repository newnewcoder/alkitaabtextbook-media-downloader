import requests as rq
import os
import shutil
import youtube_dl
from bs4 import BeautifulSoup as Bs
import html

download_dir = os.path.abspath(os.getenv("DOWNLOAD_DIR", "./files"))
url = "https://alkitaabtextbook.com/alifbaa/3e/unit1/"
response = rq.get(url)
html_doc = response.text
soup = Bs(response.text, "html.parser")
figures = soup.select("div.entry-content figure")
for figur in figures:
    file_name = figur.figcaption.text
    print(file_name)
    if 'wp-block-audio' in figur['class']:
        print('go download mp3')
        mp3_url = figur.audio['src']
        print('url=' + mp3_url)
        with rq.get(mp3_url, stream=True) as r:
            with open(download_dir + '/' + file_name + '.mp3', 'wb') as f:
                shutil.copyfileobj(r.raw, f)
    else:
        print('go download yt')
        yt_url = html.unescape(figur.div.span.iframe['src'])
        print('url=' + yt_url)
        ytdl_opts = {
            'outtmpl': download_dir + '/' + file_name + '.mp4',
            'ignoreerrors': True,
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        }
        with youtube_dl.YoutubeDL(ytdl_opts) as ydl:
            ydl.download([yt_url])
