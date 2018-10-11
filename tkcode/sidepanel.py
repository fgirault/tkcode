"""base tools for side panels"""

import tkinter as tk
from tkinter import ttk

# pylint: disable=too-many-ancestors


class SidePanel(ttk.Frame):
    """base class for side panels """

    TITLE = "UNTITLED PANEL"

    ICON_PATH = "explorer_inactive.png"

    def __init__(self, parent):
        super().__init__(parent, style="SidePanel.TFrame")
        ttk.Label(self, text=self.TITLE, style="SidePanel.Label").pack(
            side=tk.TOP, anchor=tk.W, padx=12, pady=12
        )
