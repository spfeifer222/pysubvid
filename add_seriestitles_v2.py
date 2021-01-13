#!/usr/bin/env python

from pathlib import Path
import re


class ReTitle:

    TITLE_PATTERN = re.compile(r"""
                                .*?       # everything, non-greedy
                                [- ]+     # at least 1x
                                ([^.]*)   # group1: title
                                .*?       # everything, non-greedy
                                \.srt     # .<file type>
                                """, re.UNICODE|re.VERBOSE)

    x_PATTERN = re.compile(r"""
                                (\d{0,1})     # Group1: Seriennummer 0 oder 00
                                x             # Trenner
                                (\d{2})       # group2: Episondennummer 00
                                """, re.UNICODE|re.VERBOSE)

    SE_pattern =   re.compile(r"""
                               .*?        # everything, non-greedy
                               [sS]       # s or S
                               (\d+)    # group1: series number
                               [eE]       # e or E
                               (\d+)      # group2: episode number
                               .*         # everything
                               """, re.UNICODE|re.VERBOSE)


    def __init__(self, srt_file_path, title_pattern=TITLE_PATTERN,
                 number_pattern=SE_pattern):

                 self.srt = srt_file_path
                 self.title_pattern = title_pattern
                 self.number_pattern = number_pattern



    def get_title(self):
        return self.title_pattern.search(self.srt).group(1)

    def get_series(self):
        return self.number_pattern.search(self.srt).group(1)

    def get_episode(self):
        return self.number_pattern.search(self.srt).group(2)

# initiate ReTitle class
trek = ReTitle()

# try to get series & episode number & title
files =  [file for file in Path(trek.source).iterdir() if file.is_file()]

for file in files:
    title = trek.get_title(str(file))
    print(title)

"""    file = Path(file)
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
"""
'''

    # read frim
    if re.search(SE_pattern):
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

'''
