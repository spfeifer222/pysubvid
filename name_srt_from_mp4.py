#! python
import re
from pathlib import Path

DIR = '/home/pfeifer/Multimedia/Filme@LP/Carmen Sandiego'
SE = re.compile(r"""
                    [s]*          # S for Series
                    (\d{0,1})     # Group1: Seriennummer 0 oder 00
                    [xe]{1}       # E for Episode or x
                    (\d{2})       # group2: Episondennummer 00
                """, re.X|re.I)
SE_small = re.compile(r"""
                    [s]*          # small s for Series
                    (\d{0,1})     # Group1: Seriennummer 0 oder 00
                    [xe]{1}       # small E for Episode or small x
                    (\d{2})       # group2: Episondennummer 00
                """, re.X)

for file in Path(DIR).glob('*.mp4'):

    srt_name = file.with_suffix('.srt')

    if SE_small.search(str(srt_name)):

        SE_small.sub('S\1E\2', str(srt_name))

    if not srt_name.exists():

        numbers = SE.search(str(srt_name))
        series = f"{int(numbers.group(1)):02}"
        episode = f"{int(numbers.group(2)):02}"
        [(print(f"{srt_file.name} renamed to: {srt_name.name}"), srt_file.rename(srt_name)) for srt_file in Path(DIR).glob(f"*[Ss]{series}[Ee]{episode}*.srt")]

    else:

        print(f"{srt_name.name} already exists. (Skipped)")
