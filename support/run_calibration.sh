#!/bin/bash

source ~/.virtualenvs/cv/bin/activate

# since we are now in .tmp, go up
python ../camera_relative_position.py "$@"