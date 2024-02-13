# MULTIPLE WEBCAM RECORDING FOR 3D TRACKING

## Introduction
In some of the modules on envisionBox we perform 3D tracking on multiple cameras that are recording synchronously. Before we started using those types of methods, we found that it is non-trivial to do actual recordings from multiple cameras in a synchronous way. Therefore we share a script here that allows to record from three webcams while also streaming information about the framenumbers to an LSL stream.

Through trial and error, we found that ffmpegcv was the most stable solution for recording 3 webcams simultaneously in a synchronous way. A good way to test whether your webcams are synchronous is holding a stopwatch in front of all cameras, recording the videos, and compare for each frame if all videos show the same time.

This project offers a script to record a behaviour on multiple cameras. This can be used for 3D triangulation of motion tracking with, for instance, pose2sim workflow. Additionally, the script uses LSL threading to sychronize the webcam stream with other recorded signals (e.g., audio)

## Was this helpful?
citation for this module: Kadavá, S., Snelder, J., Pouw, W. (2024). Recording from Multiple Webcams Synchronously while LSL Streaming [the day you viewed the site]. Retrieved from: https://envisionbox.org/multiple_webcam_record.html

## Contact
sarka.kadava@donders.ru.nl
