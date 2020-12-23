#!/bin/bash

EXTS=(.mp4 .avi)
dir_in="./data"
output_dir="./outputs"

for ext in ${EXTS[@]}; do
	echo "Working on extension: $ext" 
	python3 ./main.py --dir_in $dir_in --output $output_dir --extension ${ext}
	echo "pass this"
done
