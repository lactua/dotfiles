# Color Theme
#                  vvvvvvvv  change this to change theme
from themes import rosepine as theme

# General

mod = "mod4"
terminal = None # guess if None
browser = None # guess if None
file_manager = None # guess if None
launcher = "rofi -show drun"
powermenu = "rofi -show menu -modi 'menu:~/.local/share/rofi/scripts/rofi-power-menu --choices=shutdown/reboot/suspend/logout' -config ~/.config/rofi/power.rasi"
screenshots_path = "~/Pictures/screenshots/" # creates if doesn't exists
layouts_saved_file = "~/.config/qtile/layouts_saved.json" # creates if doesn't exists
autostart_file = "~/.config/qtile/autostart.sh"
wallpapers_path = "~/.local/share/wallpapers/" # creates if doesn't exists

floating_apps = [
    'nitrogen',
]

# Uncomment the first line for qwerty, the second for azerty
# num_keys = "123456789"
num_keys = "ampersand", "eacute", "quotedbl", "apostrophe", "parenleft", "minus", "egrave", "underscore", "ccedilla", "agrave"


# Groups

groups_count = 7
groups_names = list(map(str, range(1, groups_count + 1))) # Groups names **IN THE PROGRAM**, you probably don't need to change it
groups_labels = ['●' for _ in range(groups_count)] # How the groups are named in the top bar
# Alternatives :
# groups_labels = [str(i) for i in range(1, groups_count + 1)]
# groups_labels = ['what', 'ever', 'you', 'want']


# Layouts

# Uncomment to enable layout
layouts = [
    "Columns",
    # "Bsp",
    # "RatioTile",
    "MonadTall",
    "MonadWide",
    "Max",
    # "Floating",
    # "VerticalTile",
    # "Stack",
    # "Matrix",
    # "Tile",
    # "TreeTab",
    # "Zoomy",
]

layouts_margin = 10
layouts_border_width = 5
layouts_border_color = theme['disabled']
layouts_border_focus_color = theme['accent']
layouts_border_on_single = True
layouts_restore = True



# Top bar

bar_top_margin = 10
bar_bottom_margin = 10
bar_left_margin = 10
bar_right_margin = 10
bar_size = 41
bar_background_color = theme['background']
bar_foreground_color = theme['foreground']
bar_background_opacity = 1.0
bar_global_opacity = 1.0
bar_font = "Opensans Regular"
bar_nerd_font = "JetbrainsMono Nerd Font"
bar_fontsize = 13


# Widgets

widget_gap = 17
widget_left_offset = 15
widget_right_offset = 15
widget_padding = 10

widget_background_y_padding = 4.5
widget_background_x_padding = 0
widget_background_color = theme['alt_background']
widget_background_opacity = 1.0
widget_background_radius = 15
widget_background_border_color = theme['accent']
widget_background_border_width = 2.5