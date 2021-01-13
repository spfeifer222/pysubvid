## Extract Audio from Video without reencoding:

    ffmpeg -i video_input.mp4 -vn -c:a copy audio.m4a

## Strip audio stream away from video:

    ffmpeg -i video_input.mp4 -codec copy -an video.mp4

## Combine Video with Audio:

    ffmpeg -i video.mp4 -i audio.m4a -shortest -c:v copy -c:a copy final_video.mp4

## Cut at the begining of the file:

<!-->
-ss position (input/output)
           When used as an input option (before "-i"), seeks in this input file to position.
           Note that in most formats it is not possible to seek exactly, so ffmpeg will seek
           to the closest seek point before position.  When transcoding and -accurate_seek is
           enabled (the default), this extra segment between the seek point and position will
           be decoded and discarded. When doing stream copy or when -noaccurate_seek is used,
           it will be preserved.

           When used as an output option (before an output url), decodes but discards input
           until the timestamps reach position.

           position must be a time duration specification, see the Time duration section in
           the ffmpeg-utils(1) manual.
-->

