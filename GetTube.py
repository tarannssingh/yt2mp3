#!/usr/bin/env python
import pytube
from pytube import YouTube
from pytube import Channel
import sys
import os
os.environ["IMAGEIO_FFMPEG_EXE"] = "/Users/taran/Downloads/ffmpeg"
import moviepy.editor as mp 

# import yt-dlp


if len(sys.argv) != 3 or sys.argv[1] not in ["video", "music"]:
    raise ValueError("Must provide argument strictily as GetTube.py [video/music] \"[video_url]\"")

video_url = sys.argv[2]
try:
    v = YouTube(video_url)
except pytube.exceptions.RegexMatchError:
    raise ValueError(f"Video URL {video_url} does not exist")
except pytube.exceptions.VideoPrivate:
    raise ValueError(f"Video URL {video_url} is private")
except pytube.exceptions.MembersOnly:
    raise ValueError(f"Video URL {video_url} is Members Only")
except pytube.exceptions.RecordingUnavailable:
    raise ValueError(f"Video URL {video_url} does not have a recording for the livestream")
except pytube.exceptions.VideoUnavailable:
    raise ValueError(f"Video URL {video_url} does not have an available video")
except pytube.exceptions.LiveStreamError:
    raise ValueError(f"Video URL {video_url} is a livestream and cannot be downloaded")

# print(f"Title: {v.title}\nArtist: {v.author}\nViews: {v.views}\nLength: {v.length}\nRating: {v.rating}\nDescription: {v.description}\nThumbnail: {v.thumbnail_url}\nStreams: {v.streams}\n")

PATH = ""
if sys.argv[1] == "video":
    PATH = "./videos"
else: 
    PATH = "./music"
    
if not os.path.exists(PATH):
    os.mkdir(PATH)

if PATH == "./music":
    t = v.streams.filter(only_audio=True).all()
    t[0].download(PATH)
    print(f"{PATH}/{os.getcwd()}.mp4")
    video = mp.VideoFileClip(f"./{PATH}/{v.title}.mp4")
    clip = video.subclip(0, video.duration)
    clip.audio.write_audiofile(f"{PATH}/{v.title}.mp3")
    
if PATH == "./videos":
    v.streams.get_highest_resolution().download(PATH)


from pytube import Channel

# Instantiate a Channel object with the YouTube channel URL
c = Channel("https://www.youtube.com/c/SidhuMooseWalaOfficial/videos")

# Iterate through video URLs in the channel and print them
for url in c.video_urls:
    print(url)

# It seems you're attempting to download a video and print its title, 
# but you haven't defined 'v' in your code snippet.
# Assuming you want to download the first video from the channel:
video_url = c.video_urls[0]  # Get the URL of the first video
v = c.get_video(video_url)   # Get the video object
v.download()                 # Download the video
print(f"Downloaded {v.title} successfully")
print(f"Downloaded {v.title} successfully")