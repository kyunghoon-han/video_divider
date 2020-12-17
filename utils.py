import numpy as np
import cv2 as cv
import subprocess
import librosa

def write_audio(filename,output_path,bit_rate="160k", 
                sample_rate=44100, channel_num = 1):
    command = "ffmpeg -i "
    command = command + filename + " " # to read file
    command = command + "-ab " + bit_rate # bit rate assignment
    command = command + "-ac " + str(channel_num)

    in_video = ffmpeg.input(filename)
    vid = in_video.video
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

    print(vid[0])
    print()
    print(aud)

    # First read the video
    #while True:
    #    # capture frame
    #    _, frame = video.read()

