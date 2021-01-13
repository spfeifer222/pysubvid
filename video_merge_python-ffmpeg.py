#!/usr/bin/env python
# coding: utf-8

# ### IMPORT

# In[1]:


import ffmpeg
import pysubparser as ps


# ### SETTING

# In[2]:


CREATE_TESTFILE = False
#PROCESS_SRT = False

VIDEOFILE  = 'S02E01 - Samson & Delilah.de.mp4' #'S01E03 - Der Türke.mp4'
AUDIOFILE  = 'S02E01 - Samson & Delilah.en.mp4' #'S01E03 - The turk.mp4'
OUTPUTFILE = 'S02E01 - Samson & Delilah.mp4' #'S01E03 - The Turk (engl).mp4'

VIDEO_SYNCPOINT = 115.657390 # sec
AUDIO_SYNCPOINT = 114.656208 # s

AUDIO_DELAY = AUDIO_SYNCPOINT - VIDEO_SYNCPOINT

VIDEO_START = VIDEO_SYNCPOINT
AUDIO_START = VIDEO_START+AUDIO_DELAY

TEST_DURATION = 215.0 # sec


# ### GET input files

# In[3]:


video = ffmpeg.input(VIDEOFILE).video
audio = ffmpeg.input(AUDIOFILE).audio


# ### FILTERING (TESTFILE)

# In[4]:


if CREATE_TESTFILE:

    OUTPUTFILE = OUTPUTFILE[:-4] + '_TESTFILE' + OUTPUTFILE[-4:]

    video = (
        video
        .filter("trim", start=VIDEO_START, duration=TEST_DURATION)
        .filter('setpts', 'PTS-STARTPTS')
    )

    audio = (
        audio
        .filter("atrim", start=AUDIO_START, duration=TEST_DURATION)
        .filter('asetpts', 'PTS-STARTPTS')
    )


# ### FILTERING (FULL PROCESSING)

# In[5]:


if not CREATE_TESTFILE:

    video = (
        video
        .filter("trim", start=VIDEO_START)
        .filter('setpts', 'PTS-STARTPTS')
    )

    audio = (
        audio
        .filter("atrim", start=AUDIO_START)
        .filter('asetpts', 'PTS-STARTPTS')
    )


# ### JOINING

# In[6]:


joined = (
    ffmpeg
    .concat(video, audio, v=1, a=1)
)
# funktioniert:
#.concat(video, audio, v=1, a=1)
#.output(joined, OUTPUTFILE, shortest=None, acodec='copy', vcodec='copy' v , c='copy')  BELONGS to CONCAT



# ### OUTPUT

# In[7]:


(
    ffmpeg
    .output(joined, OUTPUTFILE)
    .overwrite_output()
    .run()
)


# In[8]:


# TODO: try copy streams with acodec='copy', vcodec='copy', ggf. shortest=None

