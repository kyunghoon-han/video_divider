#!/bin/bash

EXTS = ".avi .mp4"
dir_in = ""
output = ""

for ext in EXTS
do
	python3 main.py --dir_in dir_in --output output --extension ext
done
