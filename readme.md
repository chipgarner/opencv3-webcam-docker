#Docker file for Opencv with Cuda and a bash file example for using a webcam and display.

##Opencv 3.1.0 using nvidia-docker images for Cuda version 7.5 and Cudnn 3. 

See [nvidia-docker on GitHub](https://github.com/NVIDIA/nvidia-docker) for instructions for creating the cuda and cudnn images. 

A sample run command is shown in [runme.sh](runme.sh) and listed below.  This runs on Ubuntu 14.04, and probably on other linux flavors. 

GPU=0 ./nvidia-docker run --rm -it \  
  -e DISPLAY=$DISPLAY \  
  --env="QT_X11_NO_MITSHM=1" \  
  --privileged -v /dev/video0:/dev/video0 \  
  --privileged -v /tmp/.X11-unix:/tmp/.X11-unix:ro  \  
  -v /home/jkg/PycharmProjects:/dev/projects \  
   chipgarner/opencv3-webcam:python2 bash

Additional GPU's can be listed e.g. GPU=0, GPU=1. The [nvidia-docker](nvidia-docker) script replaces the docker run command.

**--env DISPLAY=$DISPLAY** sends the display id from the host to the container and probably needs to match the 0 in video0 below

**--env="QT_X11_NO_MITSHM=1"** is required by OpenCV to show the display.

**--privileged -v /dev/video0:/dev/video0**, more display stuff. This lets the container find the display. These instructions require setting xhost + on the host machine even though it uses --privileged.  I could not get the camera to work without xhost +.

**--privileged -v /tmp/.X11-unix:/tmp/.X11-unix:ro** This lets the container find the camera.

**-v /home/jkg/PycharmProjects:/dev/projects** I use this for development. This is a possibly useful example of using "volume" to make a directory on the host available in the container. Delete it or pio\\oint it to your own directories.

**chipgarner/opencv3-webcam:python2 bash** Part of the normal docker run command to start a container with a terminal running.

The camera and display only work if you call xmode + on the host system before running docker. This works great on my development machine but can be unfortunate in some situations.  I have not found a way to make the camera work with OpenCV without using xhost +. If (when) you forget to run xhost + before running the container you will see something like:  
No protocol specified  
: cannot connect to X server :0

**webacmfaces.py** is a small script that might be useful for testing that everything is working. It should run as is in the container.  It prints the OpenCV version, prints the frame rate, and outlines any faces in front of the camera.  It uses the GPU and multiple CPUs. 

