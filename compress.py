import cv2
import datetime
from pylsl import StreamInfo, StreamOutlet, local_clock
import threading
import time
import ctypes
import sys
import os
import ffmpegcv
# import signal
import tqdm


# recompress
filename = input("What is the file name? ")

vidloc = os.getcwd() + '\\data\\' + filename + '.avi' # Specify output location
# Read the written video
cap = cv2.VideoCapture(vidloc)

# Get video information
fps = cap.get(cv2.CAP_PROP_FPS)
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

# Specify the codec and create VideoWriter object for compressed video
fourcc = cv2.VideoWriter_fourcc(*'XVID')  # You can change the codec as needed
compressed_file_name = vidloc.replace('.avi', '_compr.avi')
compressed_video_writer = cv2.VideoWriter(compressed_file_name, fourcc, fps, (frame_width, frame_height))

# Display progress bar using tqdm
for _ in tqdm.tqdm(range(total_frames), desc="Compressing Video", unit="frames"):
    ret, frame = cap.read()
    if not ret:
        break
    # Compress the frame (you can apply additional compression settings if needed)
    compressed_frame = cv2.resize(frame, (frame_width, frame_height), interpolation=cv2.INTER_AREA)
    # Write the compressed frame to the VideoWriter
    compressed_video_writer.write(compressed_frame)

# Release the VideoCapture and VideoWriter resources
cap.release()
compressed_video_writer.release()

# Close the display window
cv2.destroyAllWindows()