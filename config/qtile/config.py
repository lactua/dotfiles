# Qtile config
# By rei/lactua



#   _____  _____  _____  _____  _____  _____  __     _____  _____                               
#  |  |  ||  _  || __  ||     ||  _  || __  ||  |   |   __||   __|                              
#  |  |  ||     ||    -||-   -||     || __ -||  |__ |   __||__   |                              
#   \___/ |__|__||__|__||_____||__|__||_____||_____||_____||_____| 



# Color Theme

theme = {
    'text': '#cdd6f4',
    'subtext1': '#bac2de',
    'subtext0': '#a6adc8',
    'overlay2': '#9399b2',
    'overlay1': '#7f849c',
    'overlay0': '#6c7086',
    'surface2': '#585b70',
    'surface1': '#45475a',
    'surface0': '#313244',
    'background0': '#1e1e2e',
    'background1': '#181825',
    'background2': '#11111b',
    'accent': '#89b4fa',
    'black': '#45475A',
    'red': '#F38BA8',
    'green': '#A6E3A1',
    'yellow': '#F9E2AF',
    'blue': '#89B4FA',
    'magenta': '#F5C2E7',
    'cyan': '#94E2D5',
    'white': '#BAC2DE'
}



# General

mod = "mod4"
terminal = "kitty"
browser = "firefox"
file_manager = "nautilus"
launcher = "rofi -show drun"
sceenshot_path = '~/Images/screenshots/'
layouts_saved_file = '~/.config/qtile/layouts_saved.json'
autostart_file = '~/.config/qtile/autostart.sh'

floating_apps = [
    'nitrogen',
]



# Groups

groups_count = 5 # Up to nine
# Uncomment the first line for qwerty, the second for azerty
# groups_keys = "123456789"
groups_keys = "ampersand", "eacute", "quotedbl", "apostrophe", "parenleft", "minus", "egrave", "underscore", "ccedilla", "agrave"
groups_names = map(str, range(1, groups_count + 1)) # '1234..' to groups_count



# Layouts

# Uncomment to enable layout
layouts = [
    "Columns",
    "VerticalTile",
    "RatioTile",
    "MonadWide",
    "Max",
    "Floating",
    # "Stack",
    # "Bsp",
    # "Matrix",
    # "MonadTall",
    # "Tile",
    # "TreeTab",
    # "Zoomy",
]

layouts_margin = 10
layouts_border_width = 5
layouts_border_color = theme['surface1']
layouts_border_focus_color = theme['accent']



# Top bar

bar_top_margin = 10
bar_bottom_margin = 0
bar_left_margin = 10
bar_right_margin = 10
bar_size = 37
bar_background_color = theme['background0']
bar_background_opacity = 0.85
bar_global_opacity = 1.0

widget_gap = 17
widget_left_offset = 15
widget_right_offset = 15
widget_padding = 10

widget_background_y_padding = 5
widget_background_x_padding = 0
widget_background_color = theme['background1']
widget_background_opacity = 1.0
widget_background_radius = 14







from os.path import expanduser
from subprocess import run
from os import system
from datetime import datetime
from libqtile import layout, qtile, hook, bar
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from qtile_extras import widget
from json import dump, load


#   _____  _____  _____  _____  _____  _____ 
#  |   __|| __  ||     ||  |  ||  _  ||   __|
#  |  |  ||    -||  |  ||  |  ||   __||__   |
#  |_____||__|__||_____||_____||__|   |_____|

groups = [Group(name) for name in groups_names]


#   _____  _____  _____  _____  _____  _____  _____  _____  _____ 
#  |   __||  |  ||     || __  ||_   _||     ||  |  ||_   _||   __|
#  |__   ||     ||  |  ||    -|  | |  |   --||  |  |  | |  |__   |
#  |_____||__|__||_____||__|__|  |_|  |_____||_____|  |_|  |_____|


@lazy.function
def screenshot(qtile, mode=0):
    file_path = datetime.now().strftime(f"{expanduser(sceenshot_path)}%d-%m-%Y-%H-%M-%S.jpg")
    system(f"scrot {'-s' if mode == 1 else ''} {file_path}")
    system(f"xclip -selection clipboard -t image/png -i {file_path}")

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
    Key([mod], "r", lazy.layout.normalize(), desc="Reset all window sizes"),
    Key([mod], "q", lazy.window.kill(), desc="Kill focused window"),
    Key([mod], "x", lazy.window.toggle_fullscreen(), desc="Toggle fullscreen on the focused window",),
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
    
    # Qtile
    
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),

    # Screenshot

    Key([], "Print", screenshot()),
    Key(['mod1'], "Print", screenshot(mode=1)),
    
    # Layouts

    Key([mod], "l", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod, "shift"], 'l', lazy.prev_layout(), desc="Previous layout"),

    # Groups

    Key([mod, "mod1"], "right", lazy.screen.next_group(), desc="Go to next group"),
    Key([mod, "mod1"], "left", lazy.screen.prev_group(), desc="Go to previous group"),
    *[Key([mod], groups_keys[index], lazy.group[group.name].toscreen(), desc=f"Switch to the {group.name} group") for index, group in enumerate(groups)],
    *[Key([mod, "shift"], groups_keys[index], lazy.window.togroup(group.name, switch_group=True), desc=f"Move focused window to the {group.name} group") for index, group in enumerate(groups)],

]



#   __     _____  __ __  _____  _____  _____  _____                                             
#  |  |   |  _  ||  |  ||     ||  |  ||_   _||   __|                                            
#  |  |__ |     ||_   _||  |  ||  |  |  | |  |__   |                                            
#  |_____||__|__|  |_|  |_____||_____|  |_|  |_____|  

layout_theme = {
    "border_width": layouts_border_width,
    "margin": layouts_margin,
    "border_focus": layouts_border_focus_color,
    "border_normal": layouts_border_color,
}

layouts = [getattr(layout, i)(**layout_theme) for i in layouts]



#   _____  _____  _____  _____  _____  _____  _____                                             
#  |   __||     || __  ||   __||   __||   | ||   __|                                            
#  |__   ||   --||    -||   __||   __|| | | ||__   |                                            
#  |_____||_____||__|__||_____||_____||_|___||_____|

widget_defaults = dict(
    font="Opensans",
    foreground=theme['text'],
    fontsize=13,
    padding=widget_padding,
)

extension_defaults = widget_defaults.copy()

default_background = {
    "colour": widget_background_color + hex(int(widget_background_opacity*255))[2:],
    "radius": widget_background_radius,
    "filled": True,
    "padding_y": widget_background_y_padding,
    "padding_x": widget_background_x_padding,
    "group": True
}

class WidgetTweaker:
    def __init__(self, func):
        self.format = func

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

left = [
    widget.GroupBox(
        disable_drag=True,
        borderwidth=0,
        fontsize=15,
        inactive=theme['black'],
        active=theme['white'],
        block_highlight_text_color=theme['yellow'],
        padding=7,
        decorations=[widget.decorations.RectDecoration(**default_background)],
        fmt='●'
    ),

    widget.CurrentLayout(
        fmt="Current layout : {}",
        mouse_callbacks={
            'Button2': lambda: None,
            'Button3': lazy.prev_layout()
        },
        decorations=[widget.decorations.RectDecoration(**default_background)],
    ),
]

right = [
    widget.CPU(
        format="{load_percent}%",
        fmt="󰍛   {}",
        decorations=[widget.decorations.RectDecoration(**default_background)],
    ),
        
    [
        widget.Memory(
            measure_mem="G",
            measure_swap="G",
            format="   {MemUsed: .2f}{mm} /{MemTotal: .2f}{mm}",
            decorations=[widget.decorations.RectDecoration(**default_background)],
        ),

        widget.Memory(
            measure_mem="G",
            measure_swap="G",
            format="🖴 {SwapUsed: .2f}{ms} /{SwapTotal: .2f}{ms}",
            decorations=[widget.decorations.RectDecoration(**default_background)],
        ),
    ],

    widget.Volume(
        step=2,
        fmt=volume,
        update_interval=0.01,
        limit_max_volume=True,
        decorations=[widget.decorations.RectDecoration(**default_background)],
    ),

    widget.Clock(
        format="%A %d %B %Y %H:%M",
        decorations=[widget.decorations.RectDecoration(**default_background)],
    ),

    widget.TextBox(
        '⏻',
        mouse_callbacks={
            'Button1': lazy.spawn("rofi -show menu -modi 'menu:rofi-power-menu --choices=shutdown/reboot/suspend/logout'")
        },
        decorations=[widget.decorations.RectDecoration(**default_background, extrawidth=3)],
    ),
]

for index in range(1, 2*len(left)-1, 2):
    left.insert(index, widget.Spacer(length=widget_gap))

for index in range(1, 2*len(right)-1, 2):
    right.insert(index, widget.Spacer(length=widget_gap))

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
            widgets=[widget.Spacer(length=widget_left_offset)] + left + [widget.WindowName(foreground="#00000000", fmt="")] + right + [widget.Spacer(length=widget_right_offset)],
            size=bar_size,
            background = bar_background_color + hex(int(bar_background_opacity*255))[2:],
            margin = [bar_top_margin, bar_right_margin, bar_bottom_margin, bar_left_margin],
            opacity = bar_global_opacity
        ),
    ),
]



#   _____  _____  _____  _____  _____                                                           
#  |     ||     ||  |  ||   __||   __|                                                          
#  | | | ||  |  ||  |  ||__   ||   __|                                                          
#  |_|_|_||_____||_____||_____||_____|

mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]



#   _____  _____  _____  _____  _____    _____  _____  _____  _____  _____  _____  _____  _____ 
#  |     ||_   _||  |  ||   __|| __  |  |   __||   __||_   _||_   _||     ||   | ||   __||   __|
#  |  |  |  | |  |     ||   __||    -|  |__   ||   __|  | |    | |  |-   -|| | | ||  |  ||__   |
#  |_____|  |_|  |__|__||_____||__|__|  |_____||_____|  |_|    |_|  |_____||_|___||_____||_____|

dgroups_key_binder = None
dgroups_app_rules = []
follow_mouse_focus = True
bring_front_click = True
floats_kept_above = True
cursor_warp = False
floating_layout = layout.Floating(
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
focus_on_window_activation = False
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
    run(expanduser(autostart_file))

@hook.subscribe.layout_change
def _(layout, group):
    global ready

    if ready:
        with open(expanduser(layouts_saved_file), 'r') as file:
            layouts_saved = load(file)

        layouts_saved[group.name] = layout.name

        with open(expanduser(layouts_saved_file), 'w') as file:
            dump(layouts_saved, file)

@hook.subscribe.startup
def _():
    global ready

    with open(expanduser(layouts_saved_file), 'r') as file:
        layouts_saved = load(file)

    for group in groups:
        if layouts_saved.get(group.name):
            qtile.groups_map.get(group.name).layout = layouts_saved[group.name]
    
    ready = True
