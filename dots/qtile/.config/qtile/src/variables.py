# Color Theme
#                  vvvvvvvvvvvvvvvv  change this to change theme
from themes import catppuccin_mocha as theme

# General

terminal = None # guess if None
browser = None # guess if None
file_manager = None # guess if None
launcher = "rofi -show drun"
powermenu = "rofi -show menu -modi 'menu:~/.local/share/rofi/scripts/rofi-power-menu --choices=shutdown/reboot/suspend/logout' -config ~/.config/rofi/power.rasi"
screenshots_path = "~/Pictures/screenshots/" # creates if doesn't exists
layouts_saved_file = "~/.config/qtile/cache/layouts_saved.json" # creates if doesn't exists
keybindings_file = "~/.config/qtile/src/keybindings.yaml"
wallpapers_path = "~/.local/share/wallpapers/" # creates if doesn't exists

autostarts = [
    "~/.config/qtile/src/autostart.sh",
    "~/.autostart.sh"
]

floating_apps = [
    'nitrogen',
    'loupe'
]

# Uncomment the first line for qwerty, the second for azerty
# num_keys = "123456789"
num_keys = "ampersand", "eacute", "quotedbl", "apostrophe", "parenleft", "minus", "egrave", "underscore", "ccedilla", "agrave"


# Groups

groups_count = 5
groups_labels = ['' for _ in range(groups_count)] # How the groups are named in the top bar
# Alternatives :
# groups_labels = [str(i) for i in range(1, groups_count + 1)]
# groups_labels = ['I', 'II', 'III', 'IV', 'V']



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

layouts_margin = 5
layouts_border_width = 4
layouts_border_color = theme['disabled']
layouts_border_focus_color = theme['accent']
layouts_border_on_single = True
layouts_restore = False



# Top bar

bar_top_margin = 7
bar_bottom_margin = 7
bar_left_margin = 7
bar_right_margin = 7
bar_size = 35
bar_background_color = theme['background']
bar_foreground_color = theme['foreground']
bar_background_opacity = 0.8
bar_global_opacity = 1.0
bar_border_opacity = 1.0
bar_border_width = 0
bar_border_color = theme['accent']
bar_font = "Sans-serif Medium"
bar_nerd_font = "NF"
bar_fontsize = 13


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
widget_decoration_rect_border_width = 0
widget_decoration_rect_border_color = theme["accent"]
widget_decoration_rect_padding_x = 2
widget_decoration_rect_padding_y = 4.75
widget_decoration_rect_radius = 8


# Wallpapers

wallpapers_sort_method = "creation_date"
wallpapers_randomize = False