#!/bin/bash

GPU=0 ./nvidia-docker run --rm -it \
  -e DISPLAY=$DISPLAY \
  --env="QT_X11_NO_MITSHM=1" \
  --privileged -v /dev/video0:/dev/video0 \
  --privileged -v /tmp/.X11-unix:/tmp/.X11-unix:ro  \
  -v /home/jkg/PycharmProjects:/dev/projects \
   chipgarner/opencv3-webcam:python2 bash
