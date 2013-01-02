#!/bin/bash

proyect_path=/home/luks/Escritorio/django/estable/greenphant/trainingme
dir_new_videos=/home/luks/Escritorio/django/estable/greenphant/trainingme/media/new_lesson_videos
dir_converted_videos=/home/luks/Escritorio/django/estable/greenphant/trainingme/media/converted_lesson_videos
dir_original_videos=/home/luks/Escritorio/django/estable/greenphant/trainingme/media/original_lesson_videos
servicio=ffmpeg



stamp=`date +%s`
file=/tmp/controlvideo
if [ -f  $file ]
then
	exit 0
else
	touch $file
	for n in `dir -1 $dir_new_videos`
	do
		cd $dir_new_videos
		ffmpeg -i $n -vcodec libx264 -acodec aac -strict experimental -vf "movie=Voztelecom.jpg [watermark]; [in][watermark] overlay=main_w-overlay_w-10:main_h-overlay_h-10 [out]" -vpre ipod640 $dir_converted_videos/$n-$stamp.mp4
		ffmpeg -i $n -acodec libvorbis -ac 2 -ab 96k -ar 44100 -b 345k -vf "movie=Voztelecom.jpg [watermark]; [in][watermark] overlay=main_w-overlay_w-10:main_h-overlay_h-10 [out]" -s 640x360 $dir_converted_videos/$n-$stamp.webm
		mv $dir_new_videos/$n $dir_original_videos/$stamp-$n
		cd $proyect_path
		/home/luks/Escritorio/django/estable/bin/python /home/luks/Escritorio/django/estable/greenphant/trainingme/manage.py convert original_lesson_videos/$stamp-$n new_lesson_videos/$n converted_lesson_videos/$n-$stamp.mp4 converted_lesson_videos/$n-$stamp.webm
	done
	rm $file
fi
