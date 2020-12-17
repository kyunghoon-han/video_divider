# video_divider
python codes that divides a video file to equal subdivisions (outputs the audio and a set of images separately)
# Files
## 1. utils.py
This file contains the following modules:
- `write_audio`
	- reads a video file and outputs its corresponding audio file
- `obtain_video`
	- reads a video file (no audio)
- `frame_to_audio_matcher` 
	- returns a pair of a video frame and its corresponding audio segment
- `fps_sr_matcher`
	- takes: fps of a video, expected multiplier on fps
	- formula : sr = (multiplier) * fps
- `
## 2. main.py
This reads a video file and outputs a set of directories with a frame and its corresponding audio segment
