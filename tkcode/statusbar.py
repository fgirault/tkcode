"""status bar tools """
import tkinter as tk
from tkinter import ttk

# pylint: disable=too-many-ancestors


class StatusBar(ttk.Frame):
    """A basic status bar with a label (static for now).
    TODO: be notified when command object are executed, add widgets ...
    """

    def __init__(self, parent, app):
        super().__init__(parent, style="StatusBar.TFrame")
        ttk.Label(self, text="An incredible status", style="StatusBar.TLabel").pack(
            side=tk.LEFT
        )
