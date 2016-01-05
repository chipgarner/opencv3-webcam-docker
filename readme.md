#Docker file for OpenCV with CUDA and a bash file example for using a webcam and display.

##Opencv 3.1.0 using nvidia-docker images for CUDA version 7.5 and cuDNN 3. Includes a Python 2.7 example using a webcam and face detection. Works with or without a GPU. 

The docker image is available on [Docker Hub](https://hub.docker.com/r/chipgarner/opencv3-webcam/).

A sample run command is shown in [runme.sh](runme.sh) and listed below.  This runs on Ubuntu 14.04, and probably on other linux flavors. 

xhost +

GPU=0 ./nvidia-docker run --privileged --rm -it \  
  --env DISPLAY=$DISPLAY \  
  --env="QT_X11_NO_MITSHM=1" \  
  -v /dev/video0:/dev/video0 \  
  -v /tmp/.X11-unix:/tmp/.X11-unix:ro  \  
  -v /home/jkg/PycharmProjects:/dev/projects \  
   chipgarner/opencv3-webcam:python2 bash
   
xhost -

These instructions require setting xhost + on the host machine. I could not get the camera to work without xhost +. It should be possible to enable access to only the docker container. If you are not using the camera you should be able to get the display working without xhost + using one of the methods explained [here](http://wiki.ros.org/docker/Tutorials/GUI).

Additional GPU's can be listed e.g. GPU=0, GPU=1. The [nvidia-docker](nvidia-docker) script replaces the docker run command. If you do not have an Nvidia GPU leave off the GPU=0 and use the standard docker run statement instead of ./nvida-docker run.

**--env DISPLAY=$DISPLAY** sends the display id from the host to the container.

**--env="QT_X11_NO_MITSHM=1"** is required by OpenCV to show the display.

**-v /dev/video0:/dev/video0** This lets the container find the camera.

**-v /tmp/.X11-unix:/tmp/.X11-unix:ro** This lets the container find the display via X server.

**-v /home/jkg/PycharmProjects:/dev/projects** I use this for development. This is a possibly useful example of using "volume" to make a directory on the host available in the container. Delete it or point it to your own directories.

**chipgarner/opencv3-webcam:python2 bash** Part of the normal docker run command to start a container with a terminal running. Your image will have the same name if you pulled it from [Docker Hub](https://hub.docker.com/r/chipgarner/opencv3-webcam/).

**webacmfaces.py** is a small script that might be useful for testing that everything is working. It should run as is in the container.  It prints the OpenCV version, prints the frame rate, and outlines any faces in front of the camera.  It uses the GPU and multiple CPUs. 

##Buliding the image from the Dockerfile.

###Pick your GPU/CUDA configuration:

If you have an Nvidia GPU and want to use CUDA, see [nvidia-docker on GitHub](https://github.com/NVIDIA/nvidia-docker) for instructions for creating the CUDA and cuDNN images. I am using this with Caffe for training and running neural networks and it is faster with [CUDA](https://developer.nvidia.com/cuda-zone) and [cuDNN](https://developer.nvidia.com/cudnn).  OpenCV 3.1.0 is faster with CUDA enabled (if you have one or more CUDA enabled GPUs), but cuDNN is not useful unless you are working with neural networks. The resulting image is smaller without the Nvidia images but most of the 7.6 GB is from OpenCV, and the full image will run without a GPU.

You can build the image using cuDNN and CUDA, using just CUDA or using neither if you do not have an NVIDIA GPU. As of early January 2016, the [Nvidia site](https://github.com/NVIDIA/nvidia-docker) says "Currently, only cuDNN v2 based on CUDA 7.0 is supported", however cuDNN v3 and CUDA 7.5 Dockerfiles are there and work well. cuDNN is built from CUDA, and you will need the development (devel) versions in both cases.

###Modify the Dockerfile:

Modify the Dockerfile FROM to use the appropriate image:  
    **FROM cuda:7.5-cudnn3-devel** (or whatever you called it) for cuDNN or,  
    **FROM cudnn3:latest** (your name for just CUDA without cuDNN) for CUDA 0r,  
    **FROM ubuntu:14.04** for no CUDA GPU support.
    
Modify **make -j4** on line 65, the four should be the number of cores you have and wish to use for the make. 

### Run the [docker build](https://docs.docker.com/engine/reference/commandline/build/) command:

For example:  
sudo docker build -t image-name:image-tag .

