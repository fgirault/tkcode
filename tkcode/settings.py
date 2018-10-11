""" settings module contains global variables and user settings mechanism """
import collections
import os

# application name
APP_NAME = "tkcode"

# a short description
APP_DESC = "Flat Design User Interface witk Themed Tk"

# a long description
APP_LONG_DESC = """tkcode is a text editor inspired by all those dark themed editors
like Sublime Text, Atom and VS Code that has stolen everything .. ."""

# application version
APP_VERSION = "0.0a"

# default dark palette
COLOR_DATA = dict(
    bg="#252526",  # background
    fg="#adadad",  # foreground
    sidebar_bg="#333333",  # sidebar background
    sidebar_fg="#adadad",  # sidebar foreground
    tab_bg="#1e1e1e",  # tab background
    tab_fg="#ffffff",  # tab foreground
    tab_inactive_bg="#2d2d2d",  # inactive tab background
    link="#d35400",  # link color
    status_bg="#d35400",  # status bar foreground
    status_fg="#ffffff",  # status bar background
    selected_bg="#d35400",  # active selection background
    selected_fg="#ffffff",  # active selection foreground
    text_bg="#1e1e1e",  # default text editor background
    text_fg="#eeeeee",  # default text editor foreground
)

# END OF USER SETTING

# DEVELOPER SETTINGS

# command metadata as tuple:
# label, method name to call on the app object, description (optional), shortcut (optional)
# COMMAND_DATA = [
#     ("Show Welcome", "show_welcome", "Show welcome screen"),
#     ("FILE: Open", "open_file", "Open file from filesystem", "<Control-o>"),
#     (
#         "FILE: Open folder",
#         "open_folder",
#         "Open file from filesystem",
#         "<Control-Shift-o>",
#     ),
#     ("FILE: Close", "close_file", "Open file from filesystem", "<Control-w>"),
# ]


# List of availabled palette properties
PALETTE_PROPERTIES = [
    "bg",
    "fg",
    "sidebar_bg",
    "sidebar_fg",
    "tab_bg",
    "tab_fg",
    "tab_inactive_bg",
    "link",
    "status_bg",
    "status_fg",
    "selected_bg",
    "selected_fg",
    "text_bg",
    "text_fg",
]

# A data structure that contains colors for theming
Palette = collections.namedtuple("Palette", PALETTE_PROPERTIES)

COLORS = Palette(**COLOR_DATA)

# image directory base on the path of this file
IMG_DIR = os.path.join(os.path.dirname(__file__), "img")


class Settings:
    """An api over setting data that also listen to model changes """

    def __init__(self, model, name=APP_NAME):
        self.model = model
        self.name = name

        model.add_observer(self)

    desc = property(lambda self: APP_DESC)

    long_desc = property(lambda self: APP_LONG_DESC)

    colors = property(lambda self: COLORS)

    def load(self):
        """ TODO """
        pass

    def save(self):
        """ TODO """
        pass

    def on_folder_open(self, folder):
        """demo callback"""
        print("demo callback: folder '{}'' has be opened".format(folder))
