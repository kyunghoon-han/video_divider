import argparse
import numpy as np
import utils
import cv2 as cv
import librosa 
import os, shutil

def video_paths(dir_in, extension):
    # returns the list of video files of interest 
    path_list = []
    path_so_far = dir_in
    for (path, _, files) in os.walk(dir_in):
        for a_file in files:
            if extension in a_file:
                path_list.append(os.path.join(path_so_far,a_file))
            else:
                continue 
    
    return path_list

def video_divider(file_path, output_dir, seconds=1.0,extension="npy", remove_tmp=True):
    # reads a video and saves the corresponding images 
    # and the audio files as numpy arrays
    # the argument "seconds" stands for the number of 
    # seconds for the file to be cut in
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
        os.makedirs(output_dir)
    else:
        os.makedirs(output_dir)

    video_in = cv.VideoCapture(file_path)
    fps = utils.frame_rate_calculator(video_in)
    sr = utils.frame_to_audio_matcher(fps)

    # audio to its batches
    tmp_audio_name = os.path.join(output_dir,"temp.wav")
    utils.write_audio(file_path,tmp_audio_name)
    audio, sr = librosa.core.load(tmp_audio_name,sr=sr)
    if remove_tmp:
        # cause we don't need the whole thing
        os.remove(tmp_audio_name)
    audio = utils.audio_to_batches(audio,sr * seconds)

    # now cut the videos
    counter = 0
    while True:
        for i in range(round(seconds * fps)):
            success, image = video_in.read()
            # resize the image
            image = image.reshape((1,image.shape[0], 
                                    image.shape[1], 
                                    image.shape[2]))
            if i == 0:
                img_saver = image
            else:
                img_saver = np.concatenate([img_saver,image],axis=0)
        aud_saver = audio[counter, :]

        # name the directories to save the np arrays
        save_dir_data = os.path.join(output_dir,str(counter))
        if os.path.exists(save_dir_data):
            shutil.remtree(save_dir_data)
            os.makedirs(save_dir_data)
        else:
            os.makedirs(save_dir_data)
        aud_address = os.path.join(save_dir_data,"audio.npy")
        img_address = os.path.join(save_dir_data,"image.npy")

        # save the arrays
        np.save(aud_address, aud_saver)
        np.save(img_address, img_saver)
        counter += 1
        if not success:
            break
    

# Note
# This set of codes should be able to do the following:
#   1. read multiple video files
#   2. separate the video in two: a set of images
#           and the corresponding audio
#   3. store the images and audio of same interval
#           of the video in the same folder

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
            description="Divide the input videos to its images" \
                         "and the corresponding audios. \n" \
                         "Input: video files \n" \
                         "Output: a set of folders with the following:\n" \
                         "\t 1. images of certain duration \n" \
                         "\t 2. its corresponding audio.")
    parser.add_argument('--dir_in',help='directory of input videos')
    parser.add_argument('--output_dir',help='output directory')
    parser.add_argument('--extension', help='extension of the video files')
    args = parser.parse_args()
    
    list_of_videos = video_paths(args.dir_in, args.extension)
    counter = 0
    for vid in list_of_videos:
        name_folder = os.path.join(args.output_dir,"section_"+str(counter))
        video_divider(vid,name_folder)
        counter += 1
