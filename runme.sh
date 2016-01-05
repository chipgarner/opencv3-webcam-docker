#!/bin/bash

xhost +

GPU=0 ./nvidia-docker run --privileged --rm -it \
  --env DISPLAY=$DISPLAY \
  --env="QT_X11_NO_MITSHM=1" \
  -v /dev/video0:/dev/video0 \
  -v /tmp/.X11-unix:/tmp/.X11-unix:ro  \
  -v /home/jkg/PycharmProjects:/dev/projects \
   chipgarner/opencv3-webcam:python2 bash

xhost -
