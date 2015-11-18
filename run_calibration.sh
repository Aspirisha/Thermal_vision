#/bin/bash

config_file = $1

`workon cv`

`python camera_relative_position.py $config_file`