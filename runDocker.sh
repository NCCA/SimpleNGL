#!/bin/bash
xhost +
docker build --rm -t simplengl  . 
docker run --privileged -v /tmp/.X11-unix:/tmp/.X11-unix -e DISPLAY=$DISPLAY  -it simplengl 