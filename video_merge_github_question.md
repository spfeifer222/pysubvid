```python
from moviepy.editor import VideoFileClip, AudioFileClip

VIDEOFILE = 'video_with_good_quality.mp4'
AUDIOFILE = 'video_with_origin_language.mp4'
OUTPUTFILE = 'video_with_good_quality+origin_language.mp4'
TEST_DURATION = 215.0 # sec
AUDIO_DELAY = -1.5


# from audio attribute of the VideoFileClip object
audio2 = VideoFileClip(AUDIOFILE).audio
# video including original audio
video_a = VideoFileClip(VIDEOFILE)

#create test clips (short)
# first try (without delay correction)
audio2_test = audio2.subclip(t_start=audio2.duration-TEST_DURATION, t_end=audio2.duration)
video_a_test = video_a.subclip(t_start=video_a.duration-TEST_DURATION, t_end=video_a.duration)

# combine test clips
video_va_a2 = video_a_test.set_audio(audio2_test)

# show
video_va_a2.ipython_display(maxduration=250, width=640)

#video_a_test.ipython_display(maxduration=250, width=640)  # proofed, but not synchronized: audio -1500 ms to correct

# close all instances
audio2.close()
video_a.close()
```
