#!/usr/bin/env python

import re
import argparse
import ffmpeg
from pathlib import Path
import pysubparser as ps


def verbose_print(message):

    "Print verbose messages."
    if args.verbose:
        print(message)


# GET ARGUMENTS FROM COMMANDLINE
# Create the parser
my_parser = argparse.ArgumentParser(description="Merge Audio and Video Stream of two different files. Identify pattern must be given, e.g. as S01E01 to select all files related to the first episode of the first series. It's assume that the file containing the video stream is named `<filename>.vid.<file extension>` and the file containing the audio stream `<filename>.aud.<file extension>`.")

# Add the arguments
my_parser.add_argument('pattern',
                       metavar='pattern',
                       type=str,
                       help='Pattern to identify the episode, e.g. S01E01.\nNote that this pattern must match all video files (optional: srt file) to process.')

my_parser.add_argument('-p',
                       '--path',
                       type=str,
                       default=Path.cwd(),
                       help='path to files. If no path is given, ./ is used.')

my_parser.add_argument('-sv',
                       '--syncpoint-video',
                       required=True,
                       type=float,
                       dest='VIDEO_SYNCPOINT',
                       help='Time of the first synchronous frame of VIDEOFILE in [0.000000] seconds.')

my_parser.add_argument('-sa',
                       '--syncpoint-audio',
                       required=True,
                       type=float,
                       dest='AUDIO_SYNCPOINT',
                       help='Time of the first synchronous frame of AUDIOFILE in [0.000000] seconds.')

my_parser.add_argument('-n',
                       '--name',
                       help='Name of the episode title to use in OUTPUTFILE. If no name is given, only S00E00 is included.')

my_parser.add_argument('-s',
                       '--proc_subtitle',
                       action='store_true',
                       default=False,
                       dest='PROCESS_SRT',
                       help='PROCESS_SRT (Boolean). Process srt subtile (default: False.)')

my_parser.add_argument('-o',
                       '--only_subtitle',
                       action='store_true',
                       default=False,
                       dest='ONLY_SRT',
                       help='ONLY_SRT (Boolean). Process srt subtile only, no video and audio files (default: False). Here `-sv`/`--syncpoint-video` is needed.')

my_parser.add_argument('-d',
                       '--delay-srt',
                       dest='SRT_DELAY_CORR',
                       type=float,
                       default=0.0,
                       help=' Set SRT_DELAY_CORR in [0.0] sec to counterpart known delay in srt file synchronization. Negative values reduce delay, positive values prolong delay (default: 0.0).')


my_parser.add_argument('-t',
                       '--test',
                       action='store_true',
                       default=False,
                       dest='CREATE_TESTFILE',
                       help='create a short test file to check synchronization.')

my_parser.add_argument('-v',
                       '--verbose',
                       action='store_true',
                       help='Enable verbose output.')


# Execute the parse_args() method
args = my_parser.parse_args()

#print(f"arguments: {len(list(Path(args.path).glob(f'*{args.pattern}*')))}")
verbose_print(f"\n{args}\n")


for file in Path(args.path).glob(f"*{args.pattern}*"):
    # file containing audio steam, e.g. *.aud.mp4
    if re.match(r'.*\.aud\.[\w]{3}', file.name):
        print(f"AUDIOFILE: {file}")
        AUDIOFILE = file
    # file containing video stream, e.g. *.vid.mp4
    if re.match(r'.*\.vid\.[\w]{3}', file.name):
        print(f"VIDEOFILE: {file}")
        VIDEOFILE = file
# srt subtitle file
    if re.match(r'.*\.srt$', file.name):
        print(f"SRTFILE: {file}")
        SRTFILE = file

# needed to synchronize SRT FILE
AUDIO_DELAY = args.AUDIO_SYNCPOINT - args.VIDEO_SYNCPOINT

# define in and output filenames
if args.name:
    OUTPUTFILE = Path(args.path).joinpath(args.pattern+' - '+args.name+ VIDEOFILE.suffix)
    SRTOUT = Path(args.path).joinpath(args.pattern+' - '+args.name+ '.srt')
else:
    OUTPUTFILE = Path(args.path).joinpath(args.pattern + VIDEOFILE.suffix)
    SRTOUT = Path(args.path)/SRTFILE

print(f"OUTPUTFILE: {OUTPUTFILE}")
print(f"SRTOUT: {SRTOUT}")



# skip if ONLY_SRT = True
if not args.ONLY_SRT:

    VIDEO_START = args.VIDEO_SYNCPOINT  # assume to start video at VIDEO_SYNCPOINT
    AUDIO_START = VIDEO_START+AUDIO_DELAY

    TEST_DURATION = 215.0 # seconds


    # create audio and video streams
    video = ffmpeg.input(VIDEOFILE).video
    audio = ffmpeg.input(AUDIOFILE).audio



    if args.CREATE_TESTFILE:

        OUTPUTFILE = OUTPUTFILE.name + '_TESTFILE' + OUTPUTFILE.suffix
        verbose_print(f"OUTPUTFILE: {OUTPUTFILE}")

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


    # FILTERING (FULL PROCESSING)

    if not args.CREATE_TESTFILE:

        # ffmpeg do not accept Path objects
        OUTPUTFILE = str(OUTPUTFILE)
        verbose_print(f"OUTPUTFILE: {OUTPUTFILE}")

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

    # JOINING

    joined = (
        ffmpeg
        .concat(video, audio, v=1, a=1)
    )

    # ### OUTPUT
    verbose_print(f"OUTPUTFILE [before writing process]: {OUTPUTFILE}")
    (
        ffmpeg
        .output(joined, OUTPUTFILE)
        .overwrite_output()
        .run()
    )

# SRT PROCESSING
if args.PROCESS_SRT | args.ONLY_SRT:

    # pysubparser do not accept Path objects
    SRTFILE = str(SRTFILE)
    # parse srt file
    subs = ps.parse(SRTFILE, encoding='latin-1')
    verbose_print("Parsing done")
    #SHIFT_SECONDS = -args.AUDIO_SYNCPOINT+AUDIO_DELAY+args.SRT_DELAY_CORR
    SHIFT_SECONDS = -args.AUDIO_SYNCPOINT+args.SRT_DELAY_CORR
    subs.shift(seconds=SHIFT_SECONDS)
    verbose_print(f"Shifting subtitles about {SHIFT_SECONDS} s")
    verbose_print("Subtitle shifting done")
    subs.write(path=SRTOUT)
    verbose_print("Writing done")
    print("Processing done")
    #AUDIO_DELAY_CORR
    #pass

