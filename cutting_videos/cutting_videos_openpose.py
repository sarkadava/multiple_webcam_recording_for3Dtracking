import os
from moviepy.editor import VideoFileClip, concatenate_videoclips
import cv2
import ffmpeg

# currect folder
curfolder = os.getcwd()
# parent directory
parentfolder = os.path.dirname(curfolder)

# videodata 
videodata = parentfolder + '\\xdf_procedure\\data\\Data_processed\\Data_trials\\'
# videodata = curfolder + '\\test\\'
outputfolder = curfolder + '\\output\\'
# outputfolder = curfolder + '\\test_output\\'

# load in the calibration videos (avi)
videos = []
for file in os.listdir(videodata):
    if file.endswith(".avi"):
        videos.append(os.path.join(videodata, file))

print(videos)

# keep only those that have 0_1 and 0_2 in the name
videos = [x for x in videos if '0_2' in x]
       
# def split_camera_views(input_file, output_files):
#     video = VideoFileClip(input_file)
#     # read the fps
#     frame_rate = video.fps

#     # Get the width and height of each camera view
#     width_per_camera = video.w // 3
#     height = video.h

#     # Split the video into three clips, one for each camera view
#     camera1_clip = video.subclip(0, video.duration).crop(x1=0, y1=0, x2=width_per_camera, y2=height)
#     camera2_clip = video.subclip(0, video.duration).crop(x1=width_per_camera, y1=0, x2=2 * width_per_camera, y2=height)
#     camera3_clip = video.subclip(0, video.duration).crop(x1=2 * width_per_camera, y1=0, x2=3 * width_per_camera, y2=height)

#     # Save each camera clip as a separate video file, use opencv
#     camera1_clip.write_videofile(output_files[0], fps=frame_rate, codec='libx264')
#     camera2_clip.write_videofile(output_files[1], fps=frame_rate,codec='libx264')
#     camera3_clip.write_videofile(output_files[2], fps=frame_rate,codec='libx264')

#     # Close the video objects
#     video.reader.close()

def split_camera_views(input_file, output_files):
    cap = cv2.VideoCapture(input_file)

    # Get the width and height of each camera view
    num_cameras = 3
    width_per_camera = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) // num_cameras
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frame_rate = int(cap.get(cv2.CAP_PROP_FPS))

    # Create VideoWriters for each camera
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out_cam1 = cv2.VideoWriter(output_files[0], fourcc, frame_rate, (width_per_camera, height))
    out_cam2 = cv2.VideoWriter(output_files[1], fourcc, frame_rate, (width_per_camera, height))
    out_cam3 = cv2.VideoWriter(output_files[2], fourcc, frame_rate, (width_per_camera, height))

    while True:
        ret, frame = cap.read()

        # Check if the frame is None (end of video)
        if frame is None:
            break

        # Break the frame into three parts
        camera1_frame = frame[:, :width_per_camera, :]
        camera2_frame = frame[:, width_per_camera:2*width_per_camera, :]
        camera3_frame = frame[:, 2*width_per_camera:, :]

        # Display each camera view separately (optional)
        cv2.imshow('Camera 1', camera1_frame)
        cv2.imshow('Camera 2', camera2_frame)
        cv2.imshow('Camera 3', camera3_frame)

        # Write frames to video files
        out_cam1.write(camera1_frame)
        out_cam2.write(camera2_frame)
        out_cam3.write(camera3_frame)

        if cv2.waitKey(1) == 27:
            break

    # Release VideoWriters and VideoCapture
    out_cam1.release()
    out_cam2.release()
    out_cam3.release()
    cap.release()
    cv2.destroyAllWindows()


# loop over files in folder and split them
for file in videos:
    print("working on file: "+file)
    # Get the name of the file without the extension
    filename = os.path.splitext(os.path.basename(file))[0]
    
    if 'tpose' in filename: 
        trialID = filename.split("_")[0] + "_" + filename.split("_")[1] + "_" + filename.split("_")[2]
    else:
        # session, part, trial number and participant as trial ID
        trialID = filename.split("_")[0] + "_" + filename.split("_")[1] + "_" + filename.split("_")[3] + "_" + filename.split("_")[4]
        # trialID = filename.split("_")[0] + "_" + filename.split("_")[1] + "_" + filename.split("_")[2]
    
    # create an empty folder with name of the sessionIndex
    os.makedirs(os.path.join(outputfolder, trialID))
    # inside this folder, create empty folder 'raw-2d'
    os.makedirs(os.path.join(outputfolder, trialID, 'raw-2d'))

    # create output file names, and save the three videos into the new created folder raw-2d within the sessionIndex folder
    output_files = [
        os.path.join(outputfolder, trialID, 'raw-2d', filename + '_cam1.avi'),
        os.path.join(outputfolder, trialID, 'raw-2d', filename + '_cam2.avi'),
        os.path.join(outputfolder, trialID, 'raw-2d', filename + '_cam3.avi')
    ]

    # Split the camera views
    split_camera_views(file, output_files)