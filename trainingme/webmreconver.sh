#!/bin/bash

dir_new_videos=/root/env/greenphant/trainingme/media/new_lesson_videos
dir_converted_videos=/root/env/greenphant/trainingme/media/converted_lesson_videos
dir_original_videos=/root/env/greenphant/trainingme/media/original_lesson_videos


for n in `dir -1 $dir_converted_videos | egrep '\.mp4$'`
do
    filename=`echo ${n%.*}`
    cd $dir_converted_videos
    rm $dir_converted_videos/$filename.webm
    ffmpeg -i $n -acodec libvorbis -ac 2 -ab 58k -ar 44100 -b:v 512k -threads 2 -s 1280x720 $dir_converted_videos/$filename.webm
done
