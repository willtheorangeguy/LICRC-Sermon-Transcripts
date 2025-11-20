"""
This script uses yt-dlp to download videos, by year, from the HCC
YouTube Channel sermon playlist.
"""

import yt_dlp


def download_playlist(channel_url, output_path):
    """
    Downloads all videos from a YouTube playlist.
    """
    ydl_opts = {
        "js_runtimes": {
            "deno": "/root/.deno/bin/deno",
        },
        "remote_components": {
            "ejs": "github",
        },
        "download_archive": "downloaded.txt",
        "continuedl": True,
        "nooverwrites": True,
        "format": "bestaudio",
        "extractaudio": True,
        "audioformat": "mp3",
        "audioquality": 0,
        "outtmpl": "%(upload_date>%Y)s/%(title)s.%(ext)s",
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([channel_url])


if __name__ == "__main__":
    channel_url = "https://www.youtube.com/channel/UC3RKXxa8UmArxl4ZO3QHYRw/streams"
    download_playlist(channel_url, output_path)
    print(f"Downloaded all videos from {year} to {output_path}.")
