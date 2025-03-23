#   _____       _  _   
#  |     | ___ |_|| |_ 
#  |-   -||   || ||  _|
#  |_____||_|_||_||_|  

import sys
from os.path import expanduser, exists, normpath, getctime
from subprocess import run
from os import system, listdir, makedirs
from datetime import datetime
from libqtile import layout, qtile, hook, bar
from libqtile.config import Click, Drag, Group, Key, KeyChord, Match, Screen
from libqtile.lazy import lazy
from qtile_extras import widget
from shutil import which
from json import dump, load
from yaml import safe_load

sys.path.append(expanduser('~/.config/qtile/src'))

from variables import *

screenshots_path = expanduser(screenshots_path)
layouts_saved_file = expanduser(layouts_saved_file)
keybindings_file = expanduser(keybindings_file)
wallpapers_path = expanduser(wallpapers_path)

autostarts = list(map(expanduser, autostarts))

if not exists(path := layouts_saved_file):
    with open(path, 'w') as file:
        file.write('{}')

if not exists(screenshots_path):
    makedirs(screenshots_path)

if not exists(wallpapers_path):
    makedirs(wallpapers_path)

def guess(apps):
    for app in apps:
        if which(app): break

    return app

if not terminal:
    terminal = guess([
        'alacritty',
        'kgx',
        'kconsole',
        'xterm',
        'urxvt',
        'kitty',
        'st'
    ])

if not browser:
    browser = guess([
        'zen-browser',
        'librewolf',
        'vivaldi',
        'waterfox',
        'brave',
        'firefox',
        'chromium',
        'chrome'
    ])

if not file_manager:
    file_manager = guess([
        'thunar',
        'pcmanfm',
        'nautilus',
        'dolphin'
    ])        


#  _____                          
# |   __| ___  ___  _ _  ___  ___ 
# |  |  ||  _|| . || | || . ||_ -|
# |_____||_|  |___||___||  _||___|
#                       |_|       

groups_names = list(map(str, range(1, groups_count + 1)))
groups = [Group(name) for name in groups_names]


#  __                         _        
# |  |    ___  _ _  ___  _ _ | |_  ___ 
# |  |__ | .'|| | || . || | ||  _||_ -|
# |_____||__,||_  ||___||___||_|  |___|
#             |___|                    

layout_theme = {
    "border_width": layouts_border_width,
    "margin": layouts_margin,
    "border_focus": layouts_border_focus_color,
    "border_normal": layouts_border_color,
    "border_on_single": layouts_border_on_single
}

layouts_tweaks = {
    "Columns": {
        "grow_amount": 5,
        "fair": False,
        "num_columns": 2,
    },
    "MonadTall": {
        "ratio": 0.57,
        "min_ratio": 0.5,
        "max_ratio": 0.7,
        "change_size": 20,
        "change_ratio": 0.01,
    },
    "MonadWide": {
        "ratio": 0.55,
        "min_ratio": 0.45,
        "max_ratio": 0.7,
        "change_size": 35,
        "change_ratio": 0.02,
    },
    "Bsp": {
        "fair": False,
    },
}

layouts = [getattr(layout, i)(**(layout_theme|layouts_tweaks.get(i, {}))) for i in layouts]


#  _____  _    _  _  _  _    _           
# |  |  || |_ |_|| ||_|| |_ |_| ___  ___ 
# |  |  ||  _|| || || ||  _|| || -_||_ -|
# |_____||_|  |_||_||_||_|  |_||___||___|

@lazy.function
def screenshot(_qtile, select=False, sopen=False):
    file_path = datetime.now().strftime(f"{screenshots_path}%d-%m-%Y-%H-%M-%S.jpg")
    system(f"scrot {'-fs' if select else ''} {file_path}")
    system(f"xclip -selection clipboard -t image/png -i {file_path}")
    if sopen: system(f"xdg-open {file_path} &")

class Wallpaper:
    def formatName(name):
        backslash = r"""\&~"#'{([|`^$*"""

        for c in backslash:
            name = name.replace(c, '\\'+c)
        
        return name

    def getSavedWallpaper():
        with open(expanduser('~/.config/nitrogen/bg-saved.cfg'), 'r') as file:
            path = file.read().splitlines()[1].removeprefix('file=').strip() # Get saved background path
            directory = normpath(path[::-1].split('/', 1)[1][::-1])
            name = path.split('/')[-1]

        if normpath(directory) == normpath(wallpapers_path) and name in Wallpaper.wallpapers: # Checks if the background folder is wallpapers_path is in wallpapers
            return Wallpaper.wallpapers.index(name) # Set the pointer on the saved background

    def restorePointer():
        saved = Wallpaper.getSavedWallpaper()
        if exists(expanduser('~/.config/nitrogen/bg-saved.cfg')) and saved:
            Wallpaper.current = saved 
        else:
            Wallpaper.current = 0

    def init():
        Wallpaper.wallpapers = listdir(wallpapers_path)
        Wallpaper.wallpapers.sort(key=lambda w: getctime(f"{wallpapers_path}{w}")) # Sort by creation date
        # wallpapers.sort(key=str.lower) # sort by name

        Wallpaper.mode = "zoom-fill"

        Wallpaper.restorePointer()

    def set():
        system(f'nitrogen --save --set-{Wallpaper.mode} {wallpapers_path}{Wallpaper.formatName(Wallpaper.wallpapers[Wallpaper.current])}')

    @lazy.function
    def next(_qtile):
        Wallpaper.current = (Wallpaper.current + 1) % len(Wallpaper.wallpapers)
        Wallpaper.set()

    @lazy.function
    def previous(_qtile):
        Wallpaper.current = (Wallpaper.current - 1) % len(Wallpaper.wallpapers)
        Wallpaper.set()
    
Wallpaper.init()

class WidgetTweaker:
    def __init__(self, func):
        self.format = func


#  _____  _              _              _        
# |   __|| |_  ___  ___ | |_  ___  _ _ | |_  ___ 
# |__   ||   || . ||  _||  _||  _|| | ||  _||_ -|
# |_____||_|_||___||_|  |_|  |___||___||_|  |___|

with open(keybindings_file, 'rb') as file:
    keybindings = safe_load(file)

dmod = keybindings['dmod']

keys = [
    *[Key([dmod], num_keys[index], lazy.group[group.name].toscreen()) for index, group in enumerate(groups)],
    *[Key([dmod, "shift"], num_keys[index], lazy.window.togroup(group.name, switch_group=True)) for index, group in enumerate(groups)],
]

for keybind in keybindings['Keys']:
    keys.append(Key(keybind['mods'], keybind['key'], eval(keybind['command'])))

for keychord in keybindings['Keychords']:
    submappings = [Key(k['mods'], k['key'], eval(k['command'])) for k in keychord['submappings']]

    keys.append(KeyChord(keychord['mods'], keychord['key'], submappings))


#  _____           
# | __  | ___  ___ 
# | __ -|| .'||  _|
# |_____||__,||_|  

@WidgetTweaker
def groupBox(output):
    index = groups_names.index(output)
    label = groups_labels[index]

    return label

@WidgetTweaker
def volume(output):
    if output.endswith('%'):
        volume = int(output[:-1])

        icons = {
            range(0, 33): '󰕿   ',
            range(33, 66): '󰖀   ',
            range(66, 101): '󰕾   '
        }

        icon = icons[next(filter(lambda r: volume in r, icons.keys()))]

        return icon + output
    elif output == 'M':
        return '󰕿   Muted'
    else:
        return output

@WidgetTweaker
def currentLayout(output):
    return output.capitalize()

decorations = {
    "BorderDecoration": {
        "border_width": widget_decoration_border_width,
        "colour": widget_decoration_border_color + format(int(widget_decoration_border_opacity * 255), "02x"),
        "padding_x": widget_decoration_border_padding_x,
        "padding_y": widget_decoration_border_padding_y,
    },
    "PowerLineDecoration": {
        "path": widget_decoration_powerline_path,
        "size": widget_decoration_powerline_size,
        "padding_x": widget_decoration_powerline_padding_x,
        "padding_y": widget_decoration_powerline_padding_y,
    },
    "RectDecoration": {
        "group": True,
        "filled": widget_decoration_rect_filled,
        "colour": widget_decoration_rect_color + format(int(widget_decoration_rect_opacity * 255), "02x"),
        "line_width": widget_decoration_rect_border_width,
        "line_colour": widget_decoration_rect_border_color,
        "padding_x": widget_decoration_rect_padding_x,
        "padding_y": widget_decoration_rect_padding_y,
        "radius": widget_decoration_rect_radius,
    }
}

if widget_decoration:
    decoration = [getattr(widget.decorations, widget_decoration)(**decorations[widget_decoration])]
else:
    decoration = {}

widget_defaults = dict(
    font=bar_font,
    foreground=bar_foreground_color,
    fontsize=bar_fontsize,
    padding=widget_padding,
    decorations=decoration
)

extension_defaults = widget_defaults.copy()

sep = [widget.WindowName(foreground="#00000000", fmt="", decorations=[])]
left_offset = [widget.Spacer(length=widget_left_offset, decorations=[])]
right_offset = [widget.Spacer(length=widget_right_offset, decorations=[])]
space = widget.Spacer(length=widget_gap, decorations=[])

left = [
    widget.Clock(
        format="%A %d %B %Y %H:%M",
    ), space,

    widget.TextBox(
        "\uf060",
        mouse_callbacks={
            'Button1': Wallpaper.previous(),
            'Button4': Wallpaper.next(),
            'Button5': Wallpaper.previous()
        },
    ),

    widget.TextBox(
        "Wallpaper",
        padding=0,
        mouse_callbacks={
            'Button4': Wallpaper.next(),
            'Button5': Wallpaper.previous()
        }
    ),

    widget.TextBox(
        "\uf061",
        mouse_callbacks={
            'Button1': Wallpaper.next(),
            'Button4': Wallpaper.next(),
            'Button5': Wallpaper.previous()
        },
    ), space,

    widget.Chord()
]

middle = [
    widget.GroupBox(
        font=f"{bar_font} Bold",
        disable_drag=True,
        borderwidth=0,
        fontsize=15,
        inactive=theme['disabled'],
        active=bar_foreground_color,
        block_highlight_text_color=theme['accent'],
        padding=7,
        fmt=groupBox
    ),
]

right = [
    widget.StatusNotifier(), space,
    
    widget.Volume(
        step=2,
        fmt=volume,
        mouse_callbacks={'Button1':lazy.spawn('pactl set-sink-mute @DEFAULT_SINK@ toggle')},
        update_interval=0.01,
        limit_max_volume=True,
        volume_app="pavucontrol",
    ), space,

    widget.CurrentLayout(
        fmt=currentLayout,
        mouse_callbacks={
            'Button2': lambda: None,
            'Button3': lazy.prev_layout()
        },
    ), space,

    widget.TextBox(
        '⏻',
        decorations=[] if not widget_decoration else [decoration|{'extrawidth': 3}],
        mouse_callbacks={
            'Button1': lazy.spawn(powermenu)
        },
    ), space,
]


#  _____                               
# |   __| ___  ___  ___  ___  ___  ___ 
# |__   ||  _||  _|| -_|| -_||   ||_ -|
# |_____||___||_|  |___||___||_|_||___|

screens = [
    Screen(
        top=bar.Bar(
            widgets=left_offset + left + sep + middle + sep + right + right_offset,
            size=bar_size,
            border_color=bar_border_color + format(int(bar_border_opacity * 255), "02x"),
            border_width=int(bar_border_width),
            background = bar_background_color + format(int(bar_background_opacity * 255), "02x"),
            margin = [bar_top_margin, bar_right_margin, bar_bottom_margin-layouts_margin, bar_left_margin],
            opacity = bar_global_opacity
        ),
    ),
]



#  _____                     
# |     | ___  _ _  ___  ___ 
# | | | || . || | ||_ -|| -_|
# |_|_|_||___||___||___||___|

mouse = [
    Drag([dmod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([dmod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([dmod], "Button2", lazy.window.bring_to_front()),
]


#  _____  _    _                     _____       _    _    _                
# |     || |_ | |_  ___  ___  ___   |   __| ___ | |_ | |_ |_| ___  ___  ___ 
# |  |  ||  _||   || -_||  _||_ -|  |__   || -_||  _||  _|| ||   || . ||_ -|
# |_____||_|  |_|_||___||_|  |___|  |_____||___||_|  |_|  |_||_|_||_  ||___|
#                                                                 |___|     

dgroups_key_binder = None
dgroups_app_rules = []
follow_mouse_focus = True
bring_front_click = False
floats_kept_above = True
cursor_warp = False
floating_layout = layout.Floating(
    **layout_theme,
    float_rules=[
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry,
        *[Match(wm_class=app) for app in floating_apps]
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True
auto_minimize = False
wmname = "Qtile"


#  _____            _        
# |  |  | ___  ___ | |_  ___ 
# |     || . || . || '_||_ -|
# |__|__||___||___||_,_||___|

ready = False

@hook.subscribe.startup_once
def _():
    for autostart in autostarts:
        if exists(autostart):
            run(autostart)

@hook.subscribe.layout_change
def _(layout, group):
    global ready

    if ready:
        with open(layouts_saved_file, 'r') as file:
            layouts_saved = load(file)

        layouts_saved[group.name] = layout.name

        with open(layouts_saved_file, 'w') as file:
            dump(layouts_saved, file)

@hook.subscribe.startup
def _():
    global ready

    if layouts_restore:
        with open(layouts_saved_file, 'r') as file:
            layouts_saved = load(file)

        for group in groups:
            if layouts_saved.get(group.name):
                qtile.groups_map.get(group.name).layout = layouts_saved[group.name]
    
    ready = True

@hook.subscribe.changegroup
def _():
    open("/home/lactua/gngn.txt", "w").write(str(qtile.get_groups()))