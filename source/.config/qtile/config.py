#   _____       _  _   
#  |     | ___ |_|| |_ 
#  |-   -||   || ||  _|
#  |_____||_|_||_||_|  

import sys
from os.path import expanduser, exists, normpath, getctime
from subprocess import run
from os import system, listdir, makedirs
from datetime import datetime
from libqtile import layout, qtile, hook, bar, core
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from qtile_extras import widget
from json import dump, load

sys.path.append(expanduser('~/.config/qtile'))

from variables import *

screenshots_path = expanduser(screenshots_path)
layouts_saved_file = expanduser(layouts_saved_file)
autostart_file = expanduser(autostart_file)
wallpapers_path = expanduser(wallpapers_path)

if not exists(path := layouts_saved_file):
    with open(path, 'w') as file:
        file.write('{}')

if not exists(screenshots_path):
    makedirs(screenshots_path)

if not exists(wallpapers_path):
    makedirs(wallpapers_path)

def guess(apps):
    for app in apps:
        if exists(f'/bin/{app}'): break

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
        'firefox',
        'chrome',
        'chromium',
        'librewolf',
        'vivaldi',
        'waterfox',
        'brave'
    ])

if not file_manager:
    file_manager = guess([
        'thunar',
        'pcmanfm',
        'nautilus',
        'dolphin'
    ])        


#   _____  _____  _____  _____  _____  _____ 
#  |   __|| __  ||     ||  |  ||  _  ||   __|
#  |  |  ||    -||  |  ||  |  ||   __||__   |
#  |_____||__|__||_____||_____||__|   |_____|

groups = [Group(name) for name in groups_names]


#   __     _____  __ __  _____  _____  _____  _____                                             
#  |  |   |  _  ||  |  ||     ||  |  ||_   _||   __|                                            
#  |  |__ |     ||_   _||  |  ||  |  |  | |  |__   |                                            
#  |_____||__|__|  |_|  |_____||_____|  |_|  |_____|  

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


#   _____  _____  _____  _____  _____  _____  _____  _____  _____ 
#  |   __||  |  ||     || __  ||_   _||     ||  |  ||_   _||   __|
#  |__   ||     ||  |  ||    -|  | |  |   --||  |  |  | |  |__   |
#  |_____||__|__||_____||__|__|  |_|  |_____||_____|  |_|  |_____|

@lazy.function
def screenshot(_qtile, mode=0):
    file_path = datetime.now().strftime(f"{screenshots_path}%d-%m-%Y-%H-%M-%S.jpg")
    system(f"scrot {'-s' if mode == 1 else ''} {file_path}")
    system(f"xclip -selection clipboard -t image/png -i {file_path}")

class Wallpaper:
    def formatName(name):
        backslash = r"""\&~"#'{([|`^$*"""

        for c in backslash:
            name = name.replace(c, '\\'+c)
        
        return name

    def restorePointer():
        if exists(expanduser('~/.config/nitrogen/bg-saved.cfg')):
            with open(expanduser('~/.config/nitrogen/bg-saved.cfg'), 'r') as file:
                path = file.read().splitlines()[1].removeprefix('file=').strip() # Get saved background path
                directory = normpath(path[::-1].split('/', 1)[1][::-1])
                name = path.split('/')[-1]

            if normpath(directory) == normpath(wallpapers_path) and name in Wallpaper.wallpapers: # Checks if the background folder is wallpapers_path is in wallpapers
                Wallpaper.current = Wallpaper.wallpapers.index(name) # Set the pointer on the saved background
                return
        
        Wallpaper.current = 0
        return

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


keys = [

    # Window Management

    Key([mod], "left", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "right", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "down", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "up", lazy.layout.up(), desc="Move focus up"),
    Key([mod, "shift"], "left", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "right", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "down", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "up", lazy.layout.shuffle_up(), desc="Move window up"),
    Key([mod, "control"], "left", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "right", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "down", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "up", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "j", lazy.layout.grow(), desc="Grow window"),
    Key([mod], "h", lazy.layout.shrink(), desc="Shrink window"),
    Key([mod], "r", lazy.layout.normalize(), desc="Reset all window sizes"),
    Key([mod], "q", lazy.window.kill(), desc="Kill focused window"),
    Key([mod], "m", lazy.window.toggle_fullscreen(), desc="Toggle fullscreen on the focused window",),
    
    Key([mod], "f", lazy.window.toggle_floating(), desc="Toggle floating on the focused window"),
    Key([mod], "Tab", lazy.layout.next(), desc="Move window focus to other window"),

    # Media
    
    Key([], "XF86AudioRaiseVolume", lazy.spawn('pactl set-sink-volume @DEFAULT_SINK@ +5%')),
    Key([], "XF86AudioLowerVolume", lazy.spawn('pactl set-sink-volume @DEFAULT_SINK@ -5%')),
    Key([], "XF86AudioMute", lazy.spawn('pactl set-sink-mute @DEFAULT_SINK@ toggle')),
    Key([], "XF86AudioPlay", lazy.spawn('playerctl play-pause')),
    Key([], "XF86AudioPrev", lazy.spawn('playerctl previous')),
    Key([], "XF86AudioNext", lazy.spawn('playerctl next')),

    # Launch

    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    Key([mod], "Space", lazy.spawn(launcher), desc="Launch launcher"),
    Key([mod], "b", lazy.spawn(browser), desc="Launch browser"),
    Key([mod], "e", lazy.spawn(file_manager), desc="Launch file manager"),
    Key(["control", "mod1"], "Delete", lazy.spawn(powermenu), desc="Launch powermenu"),
    
    # Qtile
    
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),

    # Screenshot

    Key([], "Print", screenshot(), desc="Take a screenshot"),
    Key(["mod1"], "Print", screenshot(mode=1), desc="Take a screenshot of a zone or a window"),

    # Wallpapers

    Key([mod], "w", Wallpaper.next(), desc="Next background"),
    Key([mod, "shift"], "w", Wallpaper.previous(), desc="Previous background"),
    
    # Layouts

    Key([mod], "l", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod, "shift"], 'l', lazy.prev_layout(), desc="Previous layout"),
    *[Key([mod, "control"], num_keys[index], lazy.group.setlayout(layout.name), desc=f"Switch to the {layout.name} layout") for index, layout in enumerate(layouts)],
    
    # Groups

    Key([mod, "mod1"], "right", lazy.screen.next_group(), desc="Go to next group"),
    Key([mod, "mod1"], "left", lazy.screen.prev_group(), desc="Go to previous group"),
    *[Key([mod], num_keys[index], lazy.group[group.name].toscreen(), desc=f"Switch to the {group.name} group") for index, group in enumerate(groups)],
    *[Key([mod, "shift"], num_keys[index], lazy.window.togroup(group.name, switch_group=True), desc=f"Move focused window to the {group.name} group") for index, group in enumerate(groups)],
]


#   _____  _____  _____  _____  _____  _____  _____                                             
#  |   __||     || __  ||   __||   __||   | ||   __|                                            
#  |__   ||   --||    -||   __||   __|| | | ||__   |                                            
#  |_____||_____||__|__||_____||_____||_|___||_____|

default_background = {
    "colour": widget_background_color + format(int(widget_background_opacity * 255), "02x"),
    "radius": widget_background_radius,
    "filled": True,
    "padding_y": widget_background_y_padding,
    "padding_x": widget_background_x_padding,
    "group": True,
}

class WidgetTweaker:
    def __init__(self, func):
        self.format = func

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

widget_defaults = dict(
    font=bar_font,
    foreground=bar_foreground_color,
    fontsize=bar_fontsize,
    padding=widget_padding,
    decorations=[widget.decorations.RectDecoration(**default_background)]
)

extension_defaults = widget_defaults.copy()

left = [
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

    widget.CurrentLayout(
        fmt="Current layout : {}",
        mouse_callbacks={
            'Button2': lambda: None,
            'Button3': lazy.prev_layout()
        },
    ),
]

right = [
    widget.CPU(
        format="{load_percent}%",
        fmt="󰍛   {}",
    ),
        
    [
        widget.TextBox(padding=3),

        widget.TextBox(
            " ",
            font=bar_nerd_font,
            padding=0
        ),

        widget.Memory(
            measure_mem="G",
            format="{MemUsed: .2f}{mm} /{MemTotal: .2f}{mm}",
            padding=0
        ),

        widget.TextBox(
            "   󰋊 ",
            font=bar_nerd_font,
            padding=0
        ),

        widget.Memory(
            measure_swap="G",
            format="{SwapUsed: .2f}{ms} /{SwapTotal: .2f}{ms}",
            padding=0
        ),

        widget.TextBox(padding=3),
    ],

    widget.Volume(
        step=2,
        fmt=volume,
        mouse_callbacks={'Button1':lazy.spawn('pactl set-sink-mute @DEFAULT_SINK@ toggle')},
        update_interval=0.01,
        limit_max_volume=True,
        volume_app="pavucontrol",
    ),

    widget.Clock(
        format="%A %d %B %Y %H:%M",
    ),

    widget.TextBox(
        '⏻',
        mouse_callbacks={
            'Button1': lazy.spawn(powermenu)
        },
        decorations=[widget.decorations.RectDecoration(**default_background | {"extrawidth": 3})],
    ),
]

for index in range(1, 2*len(left)-1, 2):
    left.insert(index, widget.Spacer(length=widget_gap, decorations=[]))

for index in range(1, 2*len(right)-1, 2):
    right.insert(index, widget.Spacer(length=widget_gap, decorations=[]))

for widget_group in filter(lambda g: isinstance(g, list), left):
    index = left.index(widget_group)
    left.pop(index)
    left = left[:index] + widget_group + left[index:]

for widget_group in filter(lambda g: isinstance(g, list), right):
    index = right.index(widget_group)
    right.pop(index)
    right = right[:index] + widget_group + right[index:]

screens = [
    Screen(
        top=bar.Bar(
            widgets=[widget.Spacer(length=widget_left_offset, decorations=[])] + left + [widget.WindowName(foreground="#00000000", fmt="", decorations=[])] + right + [widget.Spacer(length=widget_right_offset, decorations=[])],
            size=bar_size,
            background = bar_background_color + format(int(bar_background_opacity * 255), "02x"),
            margin = [bar_top_margin, bar_right_margin, bar_bottom_margin-layouts_margin, bar_left_margin],
            opacity = bar_global_opacity
        ),
    ),
]



#   _____  _____  _____  _____  _____                                                           
#  |     ||     ||  |  ||   __||   __|                                                          
#  | | | ||  |  ||  |  ||__   ||   __|                                                          
#  |_|_|_||_____||_____||_____||_____|

DPX = 50 # Distance needed to grow one time on the X axis
DPY = 25 # Distance needed to grow one time on the Y axis

last = {
    'x': 0,
    'y': 0,
    'client': ''
}

@lazy.function
def resizeClientColumnsLayout(_qtile, x, y):
    global last

    _layout = _qtile.current_group.layout

    if _layout.name != "columns":
        return

    _column = _layout.columns[_layout.current]
    _client = _column.clients[_column.current]

    if abs(last['x'] - x) >= 5 * DPX or abs(last['y'] - y) >= 5 * DPY or _client.name != last['client']: # If the window title changed or x, y anormally low -> reset last
        last = {
            'x': 0,
            'y': 0,
            'client': _client.name
        }

    delta_x = x - last['x']
    delta_y = y - last['y']
    
    for _ in range(abs(delta_x) // DPX):
        if delta_x < 0:
            _layout.grow_left()
        else:
            _layout.grow_right()

    for _ in range(abs(delta_y) // DPY):
        if delta_y < 0:
            _layout.grow_up()
        else:
            _layout.grow_down()
    
    if abs(delta_x) // DPX or abs(delta_y) >= DPY:
        last = {
            'x': x,
            'y': y,
            'client': _client.name
        }


mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
    Drag([mod, "control"], "Button3", resizeClientColumnsLayout())
]



#   _____  _____  _____  _____  _____    _____  _____  _____  _____  _____  _____  _____  _____ 
#  |     ||_   _||  |  ||   __|| __  |  |   __||   __||_   _||_   _||     ||   | ||   __||   __|
#  |  |  |  | |  |     ||   __||    -|  |__   ||   __|  | |    | |  |-   -|| | | ||  |  ||__   |
#  |_____|  |_|  |__|__||_____||__|__|  |_____||_____|  |_|    |_|  |_____||_|___||_____||_____|

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


#   _____  _____  _____  _____  _____                                                           
#  |  |  ||     ||     ||  |  ||   __|                                                          
#  |     ||  |  ||  |  ||    -||__   |                                                          
#  |__|__||_____||_____||__|__||_____| 

ready = False

@hook.subscribe.startup_once
def _():
    run(autostart_file)

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
