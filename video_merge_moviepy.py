#!/usr/bin/env python
# coding: utf-8

# In[1]:


from subprocess import Popen
from moviepy.editor import VideoFileClip, AudioFileClip

PROCESS_SRT = False

VIDEOFILE = 'S02E01 - Samson & Delilah.vid.mp4' #'S01E03 - Der Türke.mp4'
AUDIOFILE = 'S02E01 - Samson & Delilah.aud.mp4' #'S01E03 - The turk.mp4'
OUTPUTFILE = 'S02E01 - Samson & Delilah.mp4' #'S01E03 - The Turk (engl).mp4'

AUDIO_SYNCPOINT = 114.781333
VIDEO_SYNCPOINT = 115.782515
AUDIO_DELAY = AUDIO_SYNCPOINT - VIDEO_SYNCPOINT

VIDEO_START = VIDEO_SYNCPOINT  # assume to start video at VIDEO_SYNCPOINT
AUDIO_START = VIDEO_START+AUDIO_DELAY

TEST_DURATION = 215.0 # sec


#     ffmpeg -i src2 -itsoffset 20 -i src1 -c copy -map 0:v -map 1:a new.mp4
# 
# __video:__ src 2 <br> 
# __audio:__ src 1
# 
# No re-encoding takes place. In this example the audio is delayed by 20 seconds
# 
# short command to create a 300 s clip to experiment with the sync value:
# 
# ffmpeg -i src2 -itsoffset 20 -i src1 -c copy -map 0:v -map 1:a -t 300 test.mp4

# In[2]:


#merge = Popen(['ffmpeg', '-i', VIDEOFILE, '-itsoffset', f'{DELAY}', '-i', f'{AUDIOFILE}, '-c', 'copy', '-map', '0:v', '-map', '1:a', '-t', '300', 'test.mp4'], env='VIDEO')


# ### GET AUDIOfrom AUDIOFILE

# In[3]:


# create AudioFileClip object from AUDIOFILE source
audio1 = AudioFileClip(AUDIOFILE)
# from audio attribute of the VideoFileClip object
audio2 = VideoFileClip(AUDIOFILE).audio


# ### GET VIDEO from VIDEOFILE

# In[4]:


# video including original audio
video_a = VideoFileClip(VIDEOFILE)
# video with audio stripped off
video = VideoFileClip(VIDEOFILE).without_audio()


# In[5]:


#create test clips
#audio1_test = audio1.subclip(t_start=audio1.duration-TEST_DURATION+AUDIO_DELAY, t_end=audio1.duration+AUDIO_DELAY)
audio2_test = audio2.subclip(t_start=AUDIO_START)
#video_test = video.subclip(t_start=video.duration-TEST_DURATION, t_end=video.duration)
video_a_test = video_a.subclip(t_start=VIDEO_START)


# In[6]:


# combinations to create combined test clip
#video_v_a1 = video_test.set_audio(audio1_test)
#video_va_a1 = video_a_test.set_audio(audio1_test)
#video_v_a2 = video_test.set_audio(audio2_test)
video_va_a2 = video_a_test.set_audio(audio2_test)


# In[7]:


# show
#video_v_a1.ipython_display(maxduration=250, width=640)
#video_va_a1.ipython_display(maxduration=250, width=640)
#video_v_a2.ipython_display(maxduration=250, width=640)
video_va_a2.ipython_display(maxduration=250, width=640)

#video_a_test.ipython_display(maxduration=250, width=640)  # proofed, but not synchronized: audio -1500 ms to correct


# In[ ]:


# close all instances
audio1.close()
audio2.close()
video.close()
video_a.close()


# In[ ]:




