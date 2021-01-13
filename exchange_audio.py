#!/usr/bin/env python
# coding: utf-8

# Import everything needed to edit video clips
from moviepy.editor import VideoFileClip, AudioFileClip

PROCESS_SRT = False

VIDEOFILE = 'S01E03 - Der Türke.mp4'
AUDIOFILE = 'S01E03 - The turk.mp4'
OUTPUTFILE = 'S01E03 - The Turk (engl).mp4'

# Load files into clips (and select the subclip, if needed)
# string format for subclip: 'HH:MM:SS.ss'
clip_video = VideoFileClip(VIDEOFILE).subclip(t_start='00:00:39')#, t_end='')
clip_audio = AudioFileClip(AUDIOFILE).subclip(t_start='00:01:41')#, t_end='')
# Combine desired clips
video = clip_video.set_audio(clip_audio)

# Write file to disk
video.write_videofile(OUTPUTFILE)

"""
ffmpeg

Replacing audio stream
If your input video already contains audio, and you want to replace it, you need to tell ffmpeg which audio stream to take:

ffmpeg -i video.mp4 -i audio.wav -c:v copy -c:a aac -map 0:v:0 -map 1:a:0 output.mp4

The -map option makes ffmpeg only use the first video stream from the first input and the first audio stream from the second input for the output file.

see also (map): https://trac.ffmpeg.org/wiki/Map


Bsp.: map video + multiple audio:

ffmpeg -i video -i audio1 -i audio2 -i audio3 -i audio4 -i audio5 \
-map 0:v -map 1:a -map 2:a -map 3:a -map 4:a -map 5:a \
-metadata:s:a:0 language=eng -metadata:s:a:0 title="Title 1" \
-metadata:s:a:1 language=sme -metadata:s:a:1 title="Title 2" \
-metadata:s:a:2 language=ipk -metadata:s:a:2 title="Title 3" \
-metadata:s:a:3 language=nob -metadata:s:a:3 title="Title 4" \
-metadata:s:a:4 language=swa -metadata:s:a:4 title="Title 5" \
-c:v copy -c:a libopus output.mkv
