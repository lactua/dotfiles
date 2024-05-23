# Qtile config
# By rei/lactua



#   _____  _____  _____  _____  _____  _____  __     _____  _____                               
#  |  |  ||  _  || __  ||     ||  _  || __  ||  |   |   __||   __|                              
#  |  |  ||     ||    -||-   -||     || __ -||  |__ |   __||__   |                              
#   \___/ |__|__||__|__||_____||__|__||_____||_____||_____||_____| 

# General

mod = "mod4"
terminal = "kitty"
browser = "firefox"
file_manager = "nautilus"
launcher = "rofi -show drun"
sceenshot_path = '~/Images/screenshots/'

floating_apps = [
    "nitrogen"
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
    # Stack,
    # Bsp,
    # Matrix,
    # MonadTall,
    # Tile,
    # TreeTab,
    # Zoomy
]

# Theme

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
    'accent': '#89b4fa'
}









from os.path import expanduser
from subprocess import run
from datetime import datetime
from libqtile import bar, layout, qtile, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy

#   _____  _____  _____  _____  _____  _____  _____  _____  _____ 
#  |   __||  |  ||     || __  ||_   _||     ||  |  ||_   _||   __|
#  |__   ||     ||  |  ||    -|  | |  |   --||  |  |  | |  |__   |
#  |_____||__|__||_____||__|__|  |_|  |_____||_____|  |_|  |_____|

groups = [Group(name) for name in groups_names]

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
    Key([mod], "f11", lazy.window.toggle_fullscreen(), desc="Toggle fullscreen on the focused window",),
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

    Key([], "Print", lazy.spawn(f"scrot {expanduser(sceenshot_path)}%d-%m-%Y-%H-%M-%S.jpg")),

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
    "border_width": 5,
    "margin": 10,
    "border_focus": theme['accent'],
    "border_normal": theme['surface1']
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
    padding=3,
)

extension_defaults = widget_defaults.copy()

space = widget.Spacer(length=20)

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.Spacer(25),
                
                widget.GroupBox(
                    disable_drag=True,
                    this_current_screen_border=theme['accent'],
                    this_screen_border=theme['accent'],
                    borderwidth=3,
                    inactive=theme['subtext0'],
                ),
                space,
                
                widget.CurrentLayout(
                    fmt="Current layout : {}"
                ),
                space,
                
                widget.WindowName(foreground="#00000000", fmt=""), # Everything before is at left side, everything after is at right

                widget.StatusNotifier(
                    padding=10,
                ),
                space,
                
                widget.PulseVolume(
                    fmt="󰕾  {}",
                    step=1,
                    volume_app="pavucontrol"
                ),
                space,
                
                widget.Clock(
                    format="%A %d %B %Y %H:%M"
                ),
                space,

                widget.TextBox(
                    '⏻',
                    mouse_callbacks={
                        'Button1': lazy.spawn("rofi -show menu -modi 'menu:rofi-power-menu --choices=shutdown/reboot/suspend/logout'")
                    }
                ),
                
                widget.Spacer(25),
            ],
            37,
            background = "181825c0",
            corner_radius = 120,
            padding=500,
            margin = [15, 15, 3, 15],
            opacity = 1.0
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
focus_on_window_activation = "smart"
reconfigure_screens = True
auto_minimize = True
wl_input_rules = None
wmname = "Qtile"

#   _____  _____  _____  _____  _____                                                           
#  |  |  ||     ||     ||  |  ||   __|                                                          
#  |     ||  |  ||  |  ||    -||__   |                                                          
#  |__|__||_____||_____||__|__||_____| 

@hook.subscribe.startup_once
def autostart():
    autostartscript = "~/.config/qtile/autostart.sh"
    script = expanduser(autostartscript)
    run(script)
