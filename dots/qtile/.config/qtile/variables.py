# Color Theme
#                  vvvvvvvvvvvvvvvv  change this to change theme
from themes import catppuccin_mocha as theme

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

groups_count = 5
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

layouts_margin = 4
layouts_border_width = 3
layouts_border_color = theme['disabled']
layouts_border_focus_color = theme['accent']
layouts_border_on_single = True
layouts_restore = False



# Top bar

bar_top_margin = 5
bar_bottom_margin = 5
bar_left_margin = 0
bar_right_margin = 0
bar_size = 32
bar_background_color = theme['background']
bar_foreground_color = theme['foreground']
bar_background_opacity = 0
bar_global_opacity = 1.0
bar_font = "Opensans Medium"
bar_nerd_font = "JetbrainsMono Nerd Font"
bar_fontsize = 13.2


# Widgets

widget_gap = 6
widget_left_offset = 4
widget_right_offset = 4
widget_padding = 15

# Widgets Decorations

widget_decoration = "RectDecoration"

widget_decoration_border_width = 1
widget_decoration_border_color = theme['accent']
widget_decoration_border_opacity = 1.0
widget_decoration_border_padding_x = 0
widget_decoration_border_padding_y = 0

widget_decoration_powerline_path = "arrow_left"
widget_decoration_powerline_size = 10
widget_decoration_powerline_padding_x = 0
widget_decoration_powerline_padding_y = 0

widget_decoration_rect_filled = True
widget_decoration_rect_color = theme["alt_background"]
widget_decoration_rect_opacity = 1.0
widget_decoration_rect_border_width = 2.7
widget_decoration_rect_border_color = theme["accent"]
widget_decoration_rect_padding_x = 0
widget_decoration_rect_padding_y = 0
widget_decoration_rect_radius = 10
