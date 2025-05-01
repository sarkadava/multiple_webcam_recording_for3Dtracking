#!/usr/bin/python3.10

import sys
print(sys.version)
import cv2
import datetime
from pylsl import StreamInfo, StreamOutlet, local_clock
import threading
import time
import ctypes
import os
import ffmpegcv
import keyboard
# import signal
import tqdm

cams = [1, 2, 3] # change numbers if cameras not displayed

# LABSTREAMLAYER
# stream the framenumbers to the LSL 

#set sleep to 1ms accuracy
winmm = ctypes.WinDLL('winmm')
winmm.timeBeginPeriod(1)

# open the three cameras and return as variables
def open_cameras():
    cap1 = cv2.VideoCapture(cams[0], cv2.CAP_DSHOW)
    print("Camera 1 opened")
    
    cap2 = cv2.VideoCapture(cams[1], cv2.CAP_DSHOW)
    print("Camera 2 opened")
    
    cap3 = cv2.VideoCapture(cams[2], cv2.CAP_DSHOW)
    print("Camera 3 opened")

    return cap1, cap2, cap3

# MAIN CAMERA FUNCTION
def getWebcamData(cap1, cap2, cap3, video_writer):
    global frame_counter

    prev = 0
    framecounter_fr = 0
    running_framerate = 0

    # main camera loop
    while True:
        # read frames from each webcam stream
        frames = read_frames(cap1, cap2, cap3)
        if len(frames) == 1: # If read_frames returned error code, break main loop
            break
        frame_counter += 1
        outlet.push_sample([frame_counter])
        frame1, frame2, frame3 = frames
        
        # estimate the frame rate after some initial ramp up phase
        if frame_counter == 2:
            framecounter_fr += 1
            timegetfor_fr = time.time()
        elif frame_counter >= 1:
            framecounter_fr += 1
            timepassed_fr = timegetfor_fr - time.time()
            running_framerate = abs(round(framecounter_fr / timepassed_fr, 2))

        # combine frames for display and VideoWriter
        combined_frames, combined_frames_dis = combine_frames(frame1, frame2, frame3, running_framerate)

        # write combined frames to the VideoWriter
        video_writer.write(combined_frames)

        # display the combined frames
        cv2.imshow('Webcam Streams', combined_frames_dis)

        # check for the 'q' key to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_writer.release()

    # release the webcam resources
    cap1.release()
    cap2.release()
    cap3.release()

    # close the display window
    cv2.destroyAllWindows()


# read frames from 3 cameras, returns list of either frames or error code
def read_frames(cap1, cap2, cap3):
    #block and after that check for frames
    ret1, frame1 = cap1.read() # read frame camera one
    if not ret1:
        print("Can't receive frame from camera one. Exiting...")
        return [-1]
    grabbed = cap2.grab()
    if grabbed:
        ret2, frame2 = cap2.retrieve()
        if not ret2:
            print("Can't receive frame from camera one. Exiting...")
            return [-1]
    grabbed = cap3.grab()
    if grabbed:
        ret3, frame3 = cap3.retrieve()
        if not ret3:
            print("Can't receive frame from camera one. Exiting...")
            return [-1]
    return [frame1, frame2, frame3]


# combines frames to instances for display and video writer, returns instances
def combine_frames(frame1, frame2, frame3, framerate):
    # rotate the frames
    frame1 = cv2.rotate(frame1, cv2.ROTATE_90_CLOCKWISE) # rotate image
    frame2 = cv2.rotate(frame2, cv2.ROTATE_90_CLOCKWISE) # rotate image
    frame3 = cv2.rotate(frame3, cv2.ROTATE_90_CLOCKWISE) # rotate image

    # add info to show on screen
    cv2.putText(frame1, str(frame_counter), (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0))
    
    # show FPS after initial ramp up phase
    if frame_counter >= 1:
        cv2.putText(frame1, 'fps: '+ str(framerate), (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0))
    
    # resize the frames for display
    frame1_dis = cv2.resize(frame1, (240, 426), interpolation=cv2.INTER_LINEAR) # this resize results in the highest fps
    frame2_dis = cv2.resize(frame2, (240, 426), interpolation=cv2.INTER_LINEAR)
    frame3_dis = cv2.resize(frame3, (240, 426), interpolation=cv2.INTER_LINEAR)

    # combine frames horizontally
    combined_frames = cv2.hconcat([frame1, frame2, frame3])
    combined_frames_dis = cv2.hconcat([frame1_dis, frame2_dis, frame3_dis])

    return combined_frames, combined_frames_dis

################ LABSTREAMLAYER INPUTS ################
frame_rate = 60.0 # when it's set on 60, the max fps we get is around 40, if on 200, we get to 60
stream_info = StreamInfo(name='MyWebcamFrameStream', type='frameNR', channel_count=1, channel_format='int32', nominal_srate = frame_rate, source_id='MyWebcamFrameStream')
outlet = StreamOutlet(stream_info)  # broadcast the stream

################ Execute LSL threading ################

# initialize global frame counters
frame_counter = 1

# open the default webcam devices
print("Starting LSL webcam")
cap1, cap2, cap3 = open_cameras()


# specify file location of output
#pcn_id = input('Enter ID: ')
pcn_id = "1"
time_stamp = datetime.datetime.now().strftime('%Y-%m-%d')
file_name = pcn_id + '_' + time_stamp + '_output.avi'
vidloc = os.getcwd() + '\\data\\' + file_name # Specify output location
print('Data saved in: ' + vidloc)

# set up the VideoWriter
video_writer = ffmpegcv.VideoWriter(vidloc, 'rawvideo', frame_rate) # 'h264' possible, but lower quality

# initialize the LSL threads
camera_thread = threading.Thread(target=getWebcamData, args=(cap1, cap2, cap3, video_writer))
camera_thread.start()

while not keyboard.is_pressed('q'):
    time.sleep(1)

# notify when program has concluded
print("Stop")
