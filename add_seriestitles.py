#!/usr/bin/env python

from pathlib import Path
import re

S01 = {'01': '',
       '02': '',
       '03': '',
       '04': '',
       '05': '',
       '06': '',
       '07': '',
       '08': '',
       '09': '',
       '10': ''}

S02 = {'01': '',
       '02': '',
       '03': '',
       '04': '',
       '05': '',
       '06': '',
       '07': '',
       '08': '',
       '09': '',
       '10': ''}

S03 = {'01': '',
       '02': '',
       '03': '',
       '04': '',
       '05': '',
       '06': '',
       '07': '',
       '08': '',
       '09': '',
       '10': ''}

S04 = {'01': '',
       '02': '',
       '03': '',
       '04': '',
       '05': '',
       '06': '',
       '07': '',
       '08': '',
       '09': '',
       '10': ''}


series = [S01, S02, S03, S04]

def correct_format(filename):
    """
    Returns filname (str) with corrected format of series and episode
    number. Transform 0x00 format into S00E00.
    """
    SE_pattern = re.compile(r"""
                             (\d{0,1})     # Group1: Seriennummer 0 oder 00
                             x             # Trenner
                             (\d{2})       # group2: Episondennummer 00
                             """, re.UNICODE|re.VERBOSE)
    numbers = SE_pattern.search(filename)
    series = f"{int(numbers.group(1)):02}"
    episode = f"{int(numbers.group(2)):02}"
    new_name = re.sub(SE_pattern, f"S{series}E{episode}", filename)

    return new_name

def get_titles(pattern):
    """ Fill dictionaries with extracted series titles from filename."""

for ser_No, serie in enumerate(series, start=1):

    import os

    print(f"""\nser_No: {ser_No:02}""")

    if len(serie) == 0:
        # try to get titles from filenames


    else:
        titles = serie
        # looop over files of a series and add titles
        pattern = re.compile(f".*[sS]{ser_No:02}[eE](\d+).*\.(mp4|srt)")
        #for file in enumerate(sorted(Path('.').glob(pattern))):
        for file in [file for file in os.listdir('.') if pattern.search(file)]:
            file = Path(file)
            file_old = file
            ep_No = re.search(pattern, file.name).group(1)
            file_new = f"S{ser_No:02}E{ep_No}_{serie[ep_No]}{file_old.suffix}"

            if not file_old.name == file_new:
                # rename
                try:
                    file_old.rename(file_new)
                    print(f'{file_old} renamed to {file_new}.')
                except error as e:
                    print(e)
            else:
                print(f"Skip correct named file {file.name}.")

