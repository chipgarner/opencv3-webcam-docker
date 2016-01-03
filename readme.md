Docker file for Opencv 3.1.0 using nvidia-docker images for Cuda version 7.5 and 
Cudnn 3. See nvidia-docker, https://github.com/NVIDIA/nvidia-docker. 

A sample run command is listed below.  This runs on ubuntu 14.04. The nvidia-docker script replaces the docker run command (see the above reference.) One or more GPUs can be listed. The second through the fifth lines enable the display and webcam. DISPLAY is the dispaly id and probably needs to match the 0 in video0 in the next line. The fifth line lets the container find the display.

The camera and display only work if you call xmode + on the host system before running docker. I use this for development, the second to last line is an example of using "volume" to make a direcory on the host availalble in the container. Delete it or pint it to your own directories.

GPU=0 ./nvidia-docker run --rm -it \
  -e DISPLAY=$DISPLAY \
  --env="QT_X11_NO_MITSHM=1" \
  --privileged -v /dev/video0:/dev/videoO \
  --privileged -v /tmp/.X11-unix:/tmp/.X11-unix:ro  \
  -v /home/jkg/PycharmProjects:/dev/projects \
   chipgarner/opencv3-webcam:python2 bash

webacmfaces.py is a small script that might be useful for testing that everything is working. It should run as is in the container.  It prints the OpenCV version, prints the frame rate, and outlines any faces in front of the camera.  It uses the GPU and nultiple CPUs. 
