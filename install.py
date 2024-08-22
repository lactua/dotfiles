#!/bin/python3
from os import system as run, getenv, walk, mkdir, remove, unlink, link
from shutil import copy
from os.path import exists, normpath, relpath, islink, isdir, lexists
from argparse import ArgumentParser
import typing

def log(message):
    if args["verbose"]:
        print(f"{message}")

def parseArgs(**kwargs):
    parser = ArgumentParser()

    for key, args in kwargs.items():
        parser.add_argument(f"--{key}", **args)

    return parser.parse_args().__dict__

def installPackages(packages):
    run(f"{args['aurhelper']} -S --needed {str.join(' ', packages)}")

def installDependencies():
    with open("dependencies.txt", "r") as file:
        dependencies = file.read().splitlines()
    
    installPackages(dependencies)

def existingFilesChecking():
    do_for_all = False

    for path, dirs, files in walk(args["source"]):

        rpath = relpath(path, args["source"])

        for directory in map(lambda d: f"{args['target']}/{rpath}/{d}", dirs):
            if islink(directory):
                if not do_for_all:
                    if input(f"Press enter to unlink existing link: {directory} ... or type '*' to apply for all ") == "*":
                        do_for_all = True
                unlink(directory)
                log(f"Unlinked existing link: {directory}")
            
            if exists(directory) and not isdir(directory):
                if not do_for_all:
                    if input(f"Press enter to delete existing file: {directory} ...") == "*":
                        do_for_all = True
                remove(directory)
                log(f"Deleted existing file: {directory}")

        for file in map(lambda f: f"{args['target']}/{rpath}/{f}", files):
            if islink(file):
                if not do_for_all:
                    if input(f"Press enter to unlink existing link: {file} ... or type '*' to apply for all ") == "*":
                        do_for_all = True
                unlink(file)
                log(f"Unlinked existing link: {file}")
                continue

            if exists(file):
                if not do_for_all:
                    if input(f"Press enter to delete existing file: {file} ... or type '*' to apply for all ") == "*":
                        do_for_all = True
                remove(file)
                log(f"Deleted existing file: {file}")

def setup():
    for path, dirs, files in walk(args["source"]):
        rpath = relpath(path, args["source"])

        for directory in map(lambda d: f"{args['target']}/{rpath}/{d}", dirs):
            if not exists(directory):
                mkdir(directory)
                log(f"Created directory: {directory}")

        for file in files:
            if not exists(file):
                if args["link"]:
                    link(f"{path}/{file}", f"{args['target']}/{rpath}/{file}")
                    log(f"Linked file: {file} to {args['target']}/{rpath}/{file}")
                else:
                    copy(f"{path}/{file}", f"{args['target']}/{rpath}/{file}")
                    log(f"Copied file: {file} to {args['target']}/{rpath}/{file}")

def main():
    global args

    args = parseArgs(
        aurhelper={"type": str, "default": "yay", "help": "AUR helper, by default 'yay'"},
        verbose={"action": "store_true", "default": False, "help": "Display more information"},
        source={"type": str, "default":"./source", "help": "Dotfiles source"},
        target={"type": str, "default": getenv("HOME"), "help": "Dotfiles target, by default home directory"},
        link={"action": "store_true", "default": False, "help": "Creates symbolic links instead of copy files"},
        skipchecking={"action": "store_true", "default": False, "help": "Skip existing files checking"},
        skipdeps={"action": "store_true", "default": False, "help": "Skip installing dependencies"}
    )

    if not args["skipdeps"]:
        installDependencies()

    if not args["skipchecking"]:
        existingFilesChecking()

    setup()

    print("Sucessfully installed dotfiles! enjoy!")

if __name__ == "__main__":
    main()