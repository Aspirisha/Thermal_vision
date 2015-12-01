#!/bin/bash

source ~/.virtualenvs/cv/bin/activate

echo "$@" >> tmp.txt

python ~/Thermal_vision/camera_relative_position.py "$@"