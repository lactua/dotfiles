# Qtile dotfiles

## Screenshots
![](./assets/screen1.png)

## Installation
### Dependencies
Install dependencies from `dependencies.txt`
```bash
cat dependencies.txt > paru -S --needed -
```

### Dotfiles
This repo uses [**GNU Stow**](https://www.gnu.org/software/stow/) to manage dotfiles.
Enter the dots directory and stow what you want to install with `~` as target (or everything)
```bash
stow -t ~ *
```

## Configuration
I made the qtile configuration in a way that almost everything is easly tweakable without any python or qtile knowledge by editing the variables.py in the qtile config directory.

**Important** : This dotfiles is initially made for azerty keyboards so by default on a qwerty keyboard the numbers keys won't work. This can be easly changed in variables.py

## Usage

### Shortcuts

Note that shortcuts can be changed in the qtile configuration.

#### Window Management

|Key combination|Action|
|:-|:-|
|Super + h|Move focus to left|
|Super + l|Move focus to right|
|Super + j|Move focus down|
|Super + k|Move focus up|
|Super + Shift + h|Move window to the left|
|Super + Shift + l|Move window to the right|
|Super + Shift + j|Move window down|
|Super + Shift + k|Move window up|
|Super + Control + h|Grow window to the left|
|Super + Control + l|Grow window to the right|
|Super + Control + j|Grow window down|
|Super + Control + k|Grow window up|
|Super + r|Reset all window sizes|
|Super + q|Kill focused window|
|Super + m|Toggle fullscreen on the focused window|
|Super + f|Toggle floating on the focused window|
|Super + Tab|Move window focus to other window|

#### Launch

|Key combination|Action|
|:-|:-|
|Super + Return|Launch terminal|
|Super + Space|Launch launcher|
|Super + b|Launch browser|
|Super + e|Launch file manager|
|Super + Delete|Launch power menu|

#### Qtile

|Key combination|Action|
|:-|:-|
|Super + Control + r|Reload the config|
|Super + Control + q|Shutdown Qtile|

#### Screenshot

|Key combination|Action|
|:-|:-|
|Super + s|Take a screenshot|
|Super + shift + s|Take a screenshot of a selection|

#### Wallpapers
|Key combination|Action|
|:-|:-|
|Super + w|Next wallpaper|
|Super + shift + w|Previous wallpaper|

#### Layouts

|Key combination|Action|
|:-|:-|
|Super + Control + y|Next layouts|
|Super + Control + t|Previous layout|
|Super + Control + [workspace]|Switch to the specified layout|

#### Groups

|Key combination|Action|
|:-|:-|
|Super + y|Go to next group|
|Super + t|Go to previous group|
|Super + [workspace]|Switch to the specified group|
|Super + Shift + [workspace]|Move focused window to the specified group|
