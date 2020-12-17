import numpy as np
import cv2 as cv
import ffmpeg
import librosa

def no_brain_divider(filename):
    in_video = ffmpeg.input(filename)
    vid = in_video.hflip()
    aud = in_video.audio
    return vid, aud


if __name__ == '__main__':
    filename = 'conan_speech.mp4'
    vid_extension = '.mp4'
    aud_extension = '.wav'
    no_ext_name = filename.replace(vid_extension,'')
    # name the video file without the audio 
    # and the corresponding audio file
    no_audio = 'no_audio_' + no_ext_name + vid_extension
    just_aud = 'just_aud_' + no_ext_name + aud_extension
    save_dir = 'divided_stuff'

    vid, aud = no_brain_divider(filename)

    print(type(vid))
    print()
    print(type(aud))

    # First read the video
    #while True:
    #    # capture frame
    #    _, frame = video.read()

