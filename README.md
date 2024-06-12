# Qtile dotfiles

## Installation
First, clone the repository **IN YOUR HOME DIRECTORY** and cd into the clone using `git clone https://github.com/lactua/dotfiles ~/Dotfiles; cd ~/Dotfiles`

### Installing dependencies

#### Arch
```sh
cat arch_dependencies.txt | yay -S --needed -
```

#### Others

##### Base packages
Use your favorite package manager to install the packages in `dependencies.txt`

##### Qtile python modules
```sh
pip install -r python_dependencies.txt
```


### Building and installing the pijulius picom fork
In order to have animations, you have to build and install the [pijulius picom fork](https://github.com/pijulius/picom). If you don't want these animations just install the regular picom version.

### Using stow to install the dotfiles
```sh
stow .
```

## Configuration
I made the qtile configuration in a way that almost everything is easly tweakable without any python or qtile knowledge. Just edit the variables at the start of the config in the **variables** category.

**Important** : This dotfiles is initially made for azerty keyboards so by default on a qwerty keyboard the workspaces changing keys won't work. To make them work on azerty uncomment the 63 line and comment the 64.

## Usage

### Shortcuts

Note that shortcuts can be changed in the qtile configuration.

#### Window Management

|Key combination|Action|
|:-|:-|
|Super + left|Move focus to left|
|Super + right|Move focus to right|
|Super + down|Move focus down|
|Super + up|Move focus up|
|Super + Shift + left|Move window to the left|
|Super + Shift + right|Move window to the right|
|Super + Shift + down|Move window down|
|Super + Shift + up|Move window up|
|Super + Control + left|Grow window to the left|
|Super + Control + right|Grow window to the right|
|Super + Control + down|Grow window down|
|Super + Control + up|Grow window up|
|Super + r|Reset all window sizes|
|Super + q|Kill focused window|
|Super + x|Toggle fullscreen on the focused window|
|Super + f|Toggle floating on the focused window|
|Super + Tab|Move window focus to other window|

#### Media

|Key combination|Action|
|:-|:-|
|XF86AudioRaiseVolume|Increase volume by 5%|
|XF86AudioLowerVolume|Decrease volume by 5%|
|XF86AudioMute|Toggle mute|
|XF86AudioPlay|Play/Pause media|
|XF86AudioPrev|Play previous media track|
|XF86AudioNext|Play next media track|

#### Launch

|Key combination|Action|
|:-|:-|
|Super + Return|Launch terminal|
|Super + Space|Launch launcher|
|Super + b|Launch browser|
|Super + e|Launch file manager|
|Control + alt + Delete|Launch power menu|

#### Qtile

|Key combination|Action|
|:-|:-|
|Super + Control + r|Reload the config|
|Super + Control + q|Shutdown Qtile|

#### Screenshot

|Key combination|Action|
|:-|:-|
|Print|Take a screenshot|
|alt + Print|Take a screenshot in mode 1|

#### Layouts

|Key combination|Action|
|:-|:-|
|Super + l|Toggle between layouts|
|Super + Shift + l|Previous layout|
|Super + Control + [workspace]|Switch to the specified layout|

#### Groups

|Key combination|Action|
|:-|:-|
|Super + alt + right|Go to next group|
|Super + alt + left|Go to previous group|
|Super + [workspace]|Switch to the specified group|
|Super + Shift + [workspace]|Move focused window to the specified group|
