""" settings module contains global variables and user settings mechanism """
import collections
import os

APP_NAME = "tkcode"

APP_DESC = "Flat Design User Interface witk Themed Tk"

APP_LONG_DESC = """tkcode is a text editor inspired by all those dark themed editors
like Sublime Text, Atom and VS Code that has stolen everything .. ."""

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
    selected_fg="#ffffff",  # active selection background
    text_bg="#1e1e1e",  # default text editor background
    text_fg="#eeeeee",  # default text editor foreground
)


# END OF USER SETTING

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

    def __init___(self, model):

        self.model = model

        model.add_observer(self)

    name = property(lambda self: APP_NAME)

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
