#!/bin/bash
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
	for n in `dir -1 dir_new_videos`
	do
		
		cd $dir/nuevos
		ffmpeg -i $n -vcodec libx264 -acodec aac -strict experimental -vpre ipod640 $dir_converted_videos/$n-$stamp.mp4 && mv $n $dir_source_videos/$stamp-$n 
	done
	#mv $dir/nuevos/* $dir/fallidos/$stamp-$n > /dev/null
	rm $file
	/home/luks/Escritorio/django/estable/bin/python /home/luks/Escritorio/django/estable/greenphant/trainingme/manage.py prueba $n $n-$stamp.mp4
fi
