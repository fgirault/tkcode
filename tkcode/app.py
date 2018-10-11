""" tkcode.app module contains the main application class """
import os
import tkinter as tk

# observable model
import tkcode.model

# application settings
import tkcode.settings

# core components
from tkcode.commander import Commander

# register commands by importing decorated functions
import tkcode.commands

# ui theming
import tkcode.theme

# Visual components
from tkcode.sidebar import SideBar
from tkcode.editor import EditorFrame
from tkcode.statusbar import StatusBar
from tkcode.palette import PaletteFrame


class App:
    """
    Tk Code application : builds the ui and exposes an api for business logic
    like a controller
    """

    def __init__(self):
        """ constructor """

        self.model = tkcode.model.TkCodeModel()  # observable data model

        self.model.add_observer(self)

        self.settings = tkcode.settings.Settings(self.model)

        self.root = None  # tkinter Tk instance

        # The components of the interface
        self.sidebar = None
        self.notebook = None
        self.statusbar = None
        self.palette = None
        self.commander = None

        # later:
        # self.console = None

    def build_ui(self):
        """  builds the user interface """
        self.root = root = tk.Tk()
        root.title(self.settings.name)
        root.minsize(300, 300)
        root.geometry("1000x700")

        style = tkcode.theme.build_style(self.settings.colors)

        style.theme_use("tkcode")

        self.commander = Commander(self)

        root.bind("<Control-p>", self.show_palette)

        # horizontal layout for the sidebar to expand / collapse panels
        self.paned = paned = tk.ttk.PanedWindow(root, orient=tk.HORIZONTAL)
        paned.pack(fill=tk.BOTH, expand=1)

        self.sidebar = SideBar(paned, self)
        paned.add(self.sidebar)

        self.editor_frame = EditorFrame(paned, self)
        paned.add(self.editor_frame)

        self.statusbar = StatusBar(root, self)
        self.statusbar.pack(fill=tk.X, side=tk.BOTTOM)

        self.palette = PaletteFrame(self.editor_frame, self.commander)

    def run(self):
        """ launch the application """
        if not self.root:
            self.build_ui()
        self.root.mainloop()

    def after(self, delay, command):
        """ proxy method to Tk.after() """
        self.root.after(delay, command)

    def on_file_selected(self, file_obj):
        """ callback on file selection : set the window title """
        self.root.title("%s - %s" % (file_obj.basename, self.settings.name))

    # methods below are the controller methods

    def command_callable(self, name):
        """create a callable of a command """

        def _callback(*args, **kwargs):
            self.commander.run(name, *args, **kwargs)

        return _callback

    def run_command(self, name, *args, **kwargs):
        self.commander.run(name, *args, **kwargs)

    def preview_file(self, file_obj):
        self.model.set_preview(file_obj)

    def select_file(self, file_obj, originator):
        """ set a file as selected """
        self.model.set_current_file(file_obj, originator)

    def show_palette(self, event):
        """ show tool palette """
        self.palette.toggle()
