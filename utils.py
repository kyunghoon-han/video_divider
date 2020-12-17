import numpy as np
import cv2 as cv
import subprocess
import librosa

#=============================================
def write_audio(filename,output_file,bit_rate="160k", 
                sample_rate=44100, channel_num = 1):
    command = "ffmpeg -i "
    command = command + filename # to read file
    command = command + " -ab " + bit_rate # bit rate assignment
    command = command + " -ac " + str(channel_num) # channels
    command = command + " -ar " + str(sample_rate) # sample rate
    command = command + " -vn " + output_file # output
    subprocess.call(command, shell=True)

#=============================================
def frame_rate_calculator(video_in):
    # first find the OpenCV version
    (maj_ver, min_ver, submin_ver) = (cv.__version__).split('.')
    if int(maj_ver) < 3:
        fps = video_in.get(cv.cv.CV_CAP_PROP_FPS)
    else:
        fps = video_in.get(cv.CAP_PROP_FPS)
    return fps
#=============================================
def frame_to_audio_matcher(fps,multiplier=1000):
    # this returns a desired sample rate
    fps = round(fps)
    return multiplier * fps
#=============================================
if __name__ == '__main__':
    filename = 'conan_speech.mp4'
    output_aud = 'conan_speech.wav'
    # extensions
    vid_extension = '.mp4'
    aud_extension = '.wav'
    #
    no_ext_name = filename.replace(vid_extension,'')
    # name the video file without the audio 
    # and the corresponding audio file
    no_audio = 'no_audio_' + no_ext_name + vid_extension
    just_aud = 'just_aud_' + no_ext_name + aud_extension
    save_dir = 'divided_stuff'
    # read the video file
    video_in = cv.VideoCapture(filename)
    fps = frame_rate_calculator(video_in) # get fps
    sr = frame_to_audio_matcher(fps) # get expected sr

    # output an audio file 
    write_audio(filename, just_aud, sample_rate=sr)


    # First read the video
    #while True:
    #    # capture frame
    #    _, frame = video.read()

