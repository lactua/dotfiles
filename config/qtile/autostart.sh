#!/bin/sh
xrandr --output HDMI-0 --mode 1920x1080 --rate 165
setxkbmap fr
picom &
nitrogen --restore &
