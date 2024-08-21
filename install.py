#!/bin/python3
from os import system as run, getenv, walk, mkdir, remove, unlink
from os.path import exists, normpath, relpath, islink
from argparse import ArgumentParser
import typing

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
    for path, dirs, files in walk(args["source"]):
        rpath = relpath(path, args["source"])

        for directory in map(lambda d: f"{args['target']}/{rpath}/{d}", dirs):
            if islink(directory):
                input(f"Press enter to unlink existing link: {directory} ...")
                unlink(directory)

        for file in map(lambda f: f"{args['target']}/{rpath}/{f}", files):
            if islink(file):
                input(f"Press enter to unlink existing link: {file} ...")
                unlink(file)
                continue

            if exists(file):
                input(f"Press enter to delete existing file: {file} ...")
                remove(file)

def setupStow():
    run(f"stow -d {args['source']} -t {args['target']} .")

def main():
    global args

    args = parseArgs(aurhelper={"type": str, "default": "yay", "help": "AUR helper, by default 'yay'"}, source={"type": str, "default":"./source", "help": "Dotfiles source"} ,target={"type": str, "default": getenv("HOME"), "help": "Dotfiles target, by default home directory"}, skipchecking={"action": "store_true", "default": False, "help": "Skip existing files checking"}, skipdeps={"action": "store_true", "default": False, "help": "Skip installing dependencies"})

    if not args["skipdeps"]:
        installDependencies()

    if not args["skipchecking"]:
        existingFilesChecking()

    setupStow()

if __name__ == "__main__":
    main()