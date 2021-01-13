#!/usr/bin/env python
# coding: utf-8

import re
import argparse
import ffmpeg
from pathlib import Path
import pysubparser as ps

# VARIABLES

#VIDEOFILE  = 'S02E01 - Samson & Delilah.de.mp4' #'S01E03 - Der Türke.mp4'
#AUDIOFILE  = 'S02E01 - Samson & Delilah.en.mp4' #'S01E03 - The turk.mp4'
#OUTPUTFILE = 'S02E01 - Samson & Delilah.mp4' #'S01E03 - The Turk (engl).mp4'

# GET ARGUMENTS FROM COMMANDLINE

# Create the parser
my_parser = argparse.ArgumentParser(description='Merge Audio and Video Stream of two different files. Identify pattern must be given in Style S00E00. Assume that the file containing the video stream ends with *de.mp4 and the file containing the audio stream with *.en.mp4. The resulting file get the audio file name without `.en`')

# Add the arguments
my_parser.add_argument('pattern',
                       metavar='pattern',
                       type=str,
                       help='Pattern to identify the episode, e.g. S01E01.\nNote that this pattern must match all video files (optional: srt file) to process.')
my_parser.add_argument('-p',
                       '--path',
                       type=str,
                       help='path to files. If no path is given, ./ is used.')

my_parser.add_argument('-t',
                       '--test',
                       action='store_true',
                       default=False,
                       dest='CREATE_TESTFILE',
                       help='create a short test file to check synchronization.')
my_parser.add_argument('-s',
                       '--proc_subtitle',
                       action='store_true',
                       default=False,
                       dest='PROCESS_SRT',
                       help='PROCESS_SRT (Boolean). Process srt subtile (default: False.)')

my_parser.add_argument('-n',
                       '--name',
                       help='Name of the episode title to use in OUTPUTFILE. If no name is given, only S00E00 style is included.')

# Execute the parse_args() method
args = my_parser.parse_args()

#print(f"arguments: {len(list(Path(args.path).glob(f'*{args.pattern}*')))}")
print(f"\n{args}\n")

for file in Path(args.path).glob(f"*{args.pattern}*"):
    # file containing audio steam, e.g. *.en.mp4
    if re.match(r'.*\.en\.[\w]{3}', file.name):
        print(f"AUDIOFILE: {file}")
        AUDIOFILE = file
    # file containing video stream, e.g. *.de.mp4
    if re.match(r'.*\.de\.[\w]{3}', file.name):
        print(f"VIDEOFILE: {file}")
        VIDEOFILE = file
    # srt subtitle file
    if re.match(r'.*\.srt', file.name):
        print(f"SRTFILE: {file}")
        SRTFILE = file

if args.name:
    OUTPUTFILE = Path(args.path).joinpath(args.pattern+' - '+args.name+ VIDEOFILE.suffix)
else:
    OUTPUTFILE = Path(args.path).joinpath(args.pattern + VIDEOFILE.suffix)

print(f"OUTPUTFILE: {OUTPUTFILE}")

VIDEO_SYNCPOINT = input("Set VIDEO_SYNCPOINT in seconds [0.000000]: ")
AUDIO_SYNCPOINT = input("Set AUDIO_SYNCPOINT in seconds [0.000000]: ")
AUDIO_DELAY = AUDIO_SYNCPOINT - VIDEO_SYNCPOINT

VIDEO_START = VIDEO_SYNCPOINT
AUDIO_START = VIDEO_START+AUDIO_DELAY

if args.CREATE_TESTFILE:
    TEST_DURATION = input("Set lenght of TESTFILE in seconds: ")
