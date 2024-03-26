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
    
    # technology if we use youtube for link 
    t = v.streams.filter(only_audio=True).all()
    t[0].download(PATH, filename=f'{(v.title).replace(" ", "")}.mp4')
    os.chdir(f"{PATH}")
    video = mp.AudioFileClip(f'{(v.title).replace(" ", "")}.mp4').set_duration(v.length) #.without_silence()
    # video = video.remove_dead_audio(min_silence_length=10, silence_thresh=-30) 
    video.write_audiofile(f'{v.title.replace(" ", "")}.mp3')
    # audio_path = os.path.join(PATH, f"{v.title}.mp3")  # Assuming you want to save as MP3
    
    os.chdir(os.path.join(os.curdir, ".."))


if PATH == "./videos":
    v.streams.get_highest_resolution().download(PATH)
    audio = v.streams.filter(only_audio=True).all()[0]

    # get the audio clip
    audio = v.streams.filter(only_audio=True).all()[0].download(PATH, filename="test.mp4")
    os.chdir(f"{PATH}")
    # this is to properlly set the audio duration
    audio = mp.AudioFileClip(f"test.mp4").set_duration(v.length) #.without_silence()
    audio.write_audiofile(f"test.mp3") 

    # audio.write_audiofile(f"test.mp3")

    # combine the audio clip and video clip
    video = mp.VideoFileClip(f"{v.title}.mp4")
    audioclip = mp.CompositeAudioClip([mp.AudioFileClip(f"test.mp3")])
    video.audio = audioclip
    video.write_videofile(f"{v.title}-video.mp4")

    os.chdir(os.path.join(os.curdir, ".."))
    
    # print(f"{os.getcwd()}{PATH[1:]}/{v.title}.mp4")



# Instantiate a Channel object with the YouTube channel URL
# c = Channel("https://www.youtube.com/c/SidhuMooseWalaOfficial/videos")
# Iterate through video URLs in the channel and print them
# for url in c.video_urls:
#     print(url)

# It seems you're attempting to download a video and print its title, 
# but you haven't defined 'v' in your code snippet.
# Assuming you want to download the first video from the channel:
# video_url = c.video_urls[0]  # Get the URL of the first video
# v = c.get_video(video_url)   # Get the video object
# v.download()                 # Download the video
print(f"Downloaded {v.title} successfully")
