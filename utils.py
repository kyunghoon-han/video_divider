import numpy as np
import cv2 as cv
import subprocess
import librosa
import os, shutil

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
# audio and video parameters
def frame_rate_calculator(video_in):
    # first find the OpenCV version
    (maj_ver, min_ver, submin_ver) = (cv.__version__).split('.')
    if int(maj_ver) < 3:
        fps = video_in.get(cv.cv.CV_CAP_PROP_FPS)
    else:
        fps = video_in.get(cv.CAP_PROP_FPS)
    return fps

def frame_to_audio_matcher(fps,multiplier=1000):
    # this returns a desired sample rate
    fps = round(fps)
    return multiplier * fps

#=============================================
# audio modifiers
def audio_to_batches(audio, batch_size):
    audio = np.ndarray.flatten(audio).tolist()
    output_list = []
    batch_size = round(batch_size)
    for i in range(0,len(audio),batch_size):
        tmp = audio[i:i+batch_size]
        diff_len = batch_size - len(tmp)
        if diff_len > 0:
            tmp = tmp + [0.0]*diff_len
        output_list.append(tmp)
    return np.array(output_list)

#=============================================
if __name__ == '__main__':
    filename = 'conan_speech.mp4'
    output_aud = 'conan_speech.wav'
    # extensions
    vid_extension = '.mp4'
    aud_extension = '.wav'
    # naming...
    no_ext_name = filename.replace(vid_extension,'')
    # name the video file without the audio 
    # and the corresponding audio file
    no_audio = 'no_audio_' + no_ext_name + vid_extension
    just_aud = 'just_aud_' + no_ext_name + aud_extension
    save_dir = 'divided_stuff'
    
    if os.path.exists(save_dir):
        shutil.rmtree(save_dir)
        os.mkdir(save_dir)
    else:
        os.mkdir(save_dir)

    # read the video file
    video_in = cv.VideoCapture(filename)
    fps = frame_rate_calculator(video_in) # get fps
    sr = frame_to_audio_matcher(fps) # get expected sr
    #
    #  Some parameters
    #
    batch_size = sr # cut the batches by sampling rates
    switch = True

    # output an audio file 
    #write_audio(filename, just_aud, sample_rate=sr)
    # then read the file again and divide it in batches
    audio, sr = librosa.core.load(just_aud,sr=sr) # reload the saved audio file
    audio = audio_to_batches(audio,batch_size) # split the audio to batches
    print(audio.shape)
    print(sr)
    counter = 0
    while switch:
        for i in range(round(fps)):
            success, image = video_in.read()
            # resize the image
            image = image.reshape((1,image.shape[0],image.shape[1],image.shape[2]))
            if i == 0:
                img_saver = image
            else:
                img_saver = np.concatenate([img_saver,image],axis=0)
        aud_saver = audio[counter,:]
        # to save the data...
        save_dir_data = os.path.join(save_dir,"data_"+str(counter))
        if os.path.exists(save_dir_data):
            shutil.rmtree(save_dir_data)
            os.mkdir(save_dir_data)
        else:
            os.mkdir(save_dir_data)
        aud_address = os.path.join(save_dir_data,"audio.npy")
        img_address = os.path.join(save_dir_data,"image.npy")
        # then actually save these!
        np.save(aud_address,aud_saver)
        np.save(img_address,img_saver)
        counter += 1
        if not success:
            break


