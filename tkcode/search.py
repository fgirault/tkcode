"""search panel tools"""

import os
import tkinter as tk
from tkinter import ttk

from .sidepanel import SidePanel

from .settings import IMG_DIR

# pylint: disable=too-many-ancestors


class Search(SidePanel):
    """A search panel object.
    TODO: implement it ;)"""

    TITLE = "SEARCH"

    ICON_PATH = "search_inactive.png"

    def __init__(self, parent, app):
        super().__init__(parent)
