#!/bin/python

from os import system

remote_url = "https://github.com/pijulius/picom.git"
clone_path = "~/.cache/picom"

system(f"git clone {remote_url} {clone_path}; cd {clone_path}; meson setup --buildtype=release build; sudo ninja -C build install")
