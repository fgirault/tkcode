""" class for building tool palette """

# pylint: disable=too-many-ancestors

import tkinter as tk
from tkinter import ttk


def bind2shortcut(bind_str):
    """Convert tk key name to ui name """
    shortcut = []
    trans = {"Control": "Ctrl"}
    bind_str = bind_str.strip()[1:-1]
    for key_name in bind_str.split("-"):
        shortcut.append(trans.get(key_name, key_name))
    return "+".join(shortcut)


class CommandFrame(ttk.Frame):
    """a frame with information about a command"""

    def __init__(self, parent, command):
        super().__init__(parent, padding=(5, 5, 5, 8))
        self.command = command
        self.label = ttk.Label(self, text=command.title)
        self.label.pack(side=tk.LEFT, anchor=tk.W)
        self.shortcut = None
        if command.shortcut:
            self.shortcut = ttk.Label(self, text=bind2shortcut(command.shortcut))
            self.shortcut.pack(side=tk.RIGHT, anchor=tk.E)

        self.selected = False

    def set_selected(self, selected=True):
        """set the visual aspect according to the selected argument """
        self.selected = selected
        if selected:
            self.configure(style="PaletteSelected.TFrame")
            self.label.configure(style="PaletteSelected.TLabel")
            if self.shortcut:
                self.shortcut.configure(style="PaletteSelected.TLabel")
        else:
            self.configure(style="")
            self.label.configure(style="")
            if self.shortcut:
                self.shortcut.configure(style="")


class PaletteFrame(ttk.Frame):
    """A class that contains a list of representation of command, with a
    search bar, a navigation with arrow keys.
    Enter launch the selected command.
    """

    def __init__(self, parent, commander):
        super().__init__(parent)

        self.commander = commander

        self.visible = False

        # input text model
        self.search_var = tk.StringVar()

        # callback on input text change
        self.search_var.trace("w", self.on_search_change)

        # input widget
        self.entry = ttk.Entry(self, textvariable=self.search_var)
        self.entry.pack(side=tk.TOP, fill=tk.X)

        # key bindings
        # hide
        self.entry.bind("<Escape>", lambda e: self.place_forget())
        # show
        self.entry.bind("<Control-p>", lambda e: self.place_forget())
        # select upper command
        self.entry.bind("<Up>", self.on_up)
        # select lower command
        self.entry.bind("<Down>", self.on_down)

        self.entry.bind("<Return>", self.on_enter)

        # list of visual command representation
        self.command_frames = []

        # current index of the selection
        self.current_command = 0

        for command in self.commander.COMMANDS:
            frame = CommandFrame(self, command)
            frame.pack(side=tk.TOP, fill=tk.X)
            self.command_frames.append(frame)

        self.results = self.command_frames[:]

    def on_search_change(self, *args, **kw):
        """callback when searched text changes"""
        results = []
        search = self.search_var.get()
        for frame in self.command_frames:
            frame.forget()
            frame.set_selected(False)
            if search:
                if search in frame.command.title.lower():
                    results.append(frame)

            else:
                results.append(frame)

        for frame in results:
            frame.pack(side=tk.TOP, fill=tk.X)

        if results:
            self.current_command = 0
            results[0].set_selected(True)
        else:
            self.current_command = -1

        self.results = results

    def on_up(self, event):
        """Select the previous command"""
        if self.current_command > 0:
            self.results[self.current_command].set_selected(False)
            self.current_command -= 1
            self.results[self.current_command].set_selected()

    def on_down(self, event):
        """Select the next command"""
        if self.current_command < len(self.results) - 1:
            self.results[self.current_command].set_selected(False)
            self.current_command += 1
            self.results[self.current_command].set_selected()

    def toggle(self):
        """show or hide depending the state """
        if self.visible:
            self.place_forget()
        else:
            self.place(relx=0.5, y=50, anchor=tk.N)
            self.entry.focus()
            self.command_frames[self.current_command].set_selected()
        self.visible = not self.visible

    def on_enter(self, event):
        """Keypress on Enter callback """
        if self.current_command > -1:
            self.place_forget()
            self.visible = False
            self.commander.run(self.command_frames[self.current_command].command)
