""" welcome module contains classes to build the welcome tab."""
import tkinter as tk
from tkinter import ttk


class LinksFrame(ttk.Frame):
    """ A container of links and label that packs vertically"""

    def __init__(self, parent, title, links=None):
        super().__init__(parent, style="Links.TFrame")
        ttk.Label(self, text=title, style="SubHeading.TLabel").pack(
            side=tk.TOP, anchor=tk.W, pady=4, padx=1
        )
        if links:
            for label, action in links:
                if action:
                    self.add_link(label, action)
                else:
                    self.add_label(label)

    def add_link(self, label, action):
        ttk.Button(self, text=label, style="Links.TButton", command=action).pack(
            side=tk.TOP, anchor=tk.W
        )

    def add_label(self, text):
        ttk.Label(self, text=text, style="Links.TLabel").pack(side=tk.TOP, anchor=tk.W)


class RecentLinksFrame(LinksFrame):
    """A frame display a list of last opened folders"""

    def __init__(self, parent, app):
        super().__init__(parent, "Recent")
        self.app = app
        app.model.add_observer(self)

    def on_folder_open(self, folder):
        """model callback"""
        self.add_link(folder.basename, lambda: self.app.open_folder(folder.path))


class WelcomeTab(ttk.Frame):
    """ A start-up screen with recent folder and useful links """

    def __init__(self, parent, app):
        super().__init__(parent, style="Welcome.TFrame", padding=[56, 12, 8, 8])
        ttk.Label(self, text=app.name, style="Heading.TLabel").pack(
            side=tk.TOP, anchor=tk.W
        )
        ttk.Label(self, text=app.desc, style="SubHeading.TLabel").pack(
            side=tk.TOP, anchor=tk.W
        )

        frame = ttk.Frame(self, style="Welcome.TFrame")
        frame.pack(fill=tk.BOTH, expand=1, pady=12)

        left_frame = ttk.Frame(frame, style="Welcome.TFrame")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        LinksFrame(
            left_frame,
            "Start",
            (
                ("Open folder ...", app.open_folder),
                ("Open file ...", app.open_file),
                ("Clone git repository ...", None),
            ),
        ).pack(side=tk.TOP, anchor=tk.W, pady=12)

        RecentLinksFrame(left_frame, app).pack(side=tk.TOP, anchor=tk.W, pady=12)

        LinksFrame(
            left_frame,
            "Help",
            (
                ("Product documentation", None),
                ("Introductory videos", None),
                ("GitHub repository", None),
                ("StackOverflow", None),
            ),
        ).pack(side=tk.TOP, anchor=tk.W, pady=12)

        right_frame = ttk.Frame(frame, style="Welcome.TFrame")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=1)
        ttk.Label(right_frame, text="Quick links", style="Links.TLabel").pack(
            side=tk.TOP, anchor=tk.W, pady=16, padx=1
        )

        LinksFrame(
            right_frame,
            "Help",
            (
                ("Product documentation", None),
                ("Introductory videos", None),
                ("GitHub repository", None),
                ("StackOverflow", None),
            ),
        ).pack(side=tk.TOP, anchor=tk.W, pady=12)
