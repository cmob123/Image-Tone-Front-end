#!/bin/bash

filename=$1
dir_suffix="_examples"
tmp_dir=$filename$dir_suffix
echo $tmp_dir
mkdir $tmp_dir

#Fixes the issue that curl has with <CR><LF>
dos2unix $filename

jpg=.jpg
zip=.zip

num=0

while read -r line
	do 
	echo $line
	echo $tmp_dir/$num$jpg
	curl -L -s -o $tmp_dir/$num$jpg $line
	num=$(($num+1))
done < "$filename"

echo "There is no zip command for Windows, so you'll have to zip the contents of this file manually"
echo "Make sure to delete the folder when you're done


#zip $filename$suffix$zip $tmp_dir/*

#rm -r $tmp_dir

