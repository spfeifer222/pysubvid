### REPLACING AUDIO STREAM (FFMPEG)

If your input video already contains audio, and you want to replace it, you need to tell ffmpeg which audio stream to take:

    ffmpeg -i video.mp4 -i audio.wav \
    -c:v copy -c:a aac -strict experimental \
    -map 0:v:0 -map 1:a:0 output.mp4

The map option makes ffmpeg only use the first video stream from the first input and the first audio stream from the second input for the output file.

### EXTRACT AUDIO FROM VIDEO FILE

To extract sound from a video file, and save it as Mp3 file, use the following command:

    $ ffmpeg -i video1.avi -vn -ar 44100 -ac 2 -ab 192 -f mp3 audio3.mp3

Explanation about the options used in above command.

Source video : video.avi
Audio bitrate : 192kb/s
output format : mp3
Generated sound : audio3.mp3

### Audio/video pipeline (python-ffmpeg example)

__Source:__ https://github.com/kkroening/ffmpeg-python/tree/master/examples

![video/audio pipeline schema](av-pipeline.png)

```
in1 = ffmpeg.input('in1.mp4')
in2 = ffmpeg.input('in2.mp4')
v1 = in1.video.hflip()
a1 = in1.audio
v2 = in2.video.filter('reverse').filter('hue', s=0)
a2 = in2.audio.filter('areverse').filter('aphaser')
joined = ffmpeg.concat(v1, a1, v2, a2, v=1, a=1).node
v3 = joined[0]
a3 = joined[1].filter('volume', 0.8)
out = ffmpeg.output(v3, a3, 'out.mp4')
out.run()
```

### Extracting a Section of a File Without Re-Encoding

__Source:__ https://www.streamingmedia.com/Articles/Editorial/Featured-Articles/Discover-the-Six-FFmpeg-Commands-You-Cant-Live-Without-133179.aspx?utm_source=related_articles&utm_medium=gutenberg&utm_campaign=editors_selection

The test file is about 12 seconds long. This command seeks to 5 seconds into the file and excerpts the next 3 seconds without re-encoding:

```bash
ffmpeg -ss 00:00:05 -i input.mp4 -t 00:00:03 -c:v copy -c:a copy excerpt.mp4
```


Code | Explanation
-----|------------
`-ss 00:00:05` | Seeks to 5 seconds into the file.
`-t 00:00:05`   | Extracts this duration of the file. If you leave this switch off, FFmpeg will include from the seek point to the end of the file in the extracted file.

__Note that FFmpeg seems to work around keyframes in the file so the _results are typically not frame-accurate_. This doesn’t matter in most instances, but if you absolutely need a specific duration or specific frames included or excluded from your excerpted file, this technique probably won’t work. In these cases, you’re better off using your video editor.__

If you want to __extract only the video__ in the file and not the audio, add the __`-an` switch__. To __extract audio only__, add the __`-vn` switch__. Note that the MP4 container can hold audio-only files, so you don’t need to change container formats when producing audio-only files from MP4 sources.

