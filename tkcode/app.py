""" tkcode.app module contains the main application class """
import os
import tkinter as tk

# may be rewrite the filedialog one day
import tkinter.filedialog as filedialog


import tkcode.settings as settings

# observable model
from .model import TkCodeModel

# Visual components
from .sidebar import SideBar
from .editor import EditorFrame
from .statusbar import StatusBar
from .palette import PaletteFrame

from .theme import build_style


class Command:
    """Base class for commands meant to be displayed in the palette """

    def __init__(self, title, command, desc="", shortcut=""):
        self.title = title
        self.command = command
        self.desc = desc
        self.shortcut = shortcut

    def execute(self, *args, **kw):
        """Execute the callable self.command"""
        self.command(*args, **kw)


class App:
    """
    Tk Code application : builds the ui and exposes an api for business logic
    like a controller
    """

    # A suffix added to the window title
    TITLE_SUFFIX = "tkcode"

    # command meta
    command_data = [
        ("Show Welcome", "show_welcome", "Show welcome screen"),
        ("FILE: Open", "open_file", "Open file from filesystem", "<Control-o>"),
        (
            "FILE: Open folder",
            "open_folder",
            "Open file from filesystem",
            "<Control-Shift-o>",
        ),
        ("FILE: Close", "close_file", "Open file from filesystem", "<Control-w>"),
    ]

    def __init__(self):
        """ constructor """
        self.name = settings.APP_NAME
        self.desc = settings.APP_DESC
        self.root = None  # tkinter Tk instance
        self.model = TkCodeModel()  # observable data model

        self.model.add_observer(self)

        # The components of the interface
        self.sidebar = None
        self.notebook = None
        self.statusbar = None
        self.console = None
        self.palette = None

        # list of command instances
        self.commands = []

    def build_ui(self):
        """  builds the user interface """
        self.root = root = tk.Tk()
        root.title(self.name)
        root.minsize(300, 300)
        root.geometry("1000x700")

        self.commands = self.build_commands(self.command_data)

        root.bind("<Control-p>", self.show_palette)

        build_style(settings.COLORS)

        # horizontal layout for the sidebar to expand / collapse panels
        self.paned = paned = tk.ttk.PanedWindow(root, orient=tk.HORIZONTAL)
        paned.pack(fill=tk.BOTH, expand=1)

        self.sidebar = SideBar(paned, self)
        paned.add(self.sidebar)

        self.editor_frame = EditorFrame(paned, self)
        paned.add(self.editor_frame)

        self.statusbar = StatusBar(root, self)
        self.statusbar.pack(fill=tk.X, side=tk.BOTTOM)

        self.palette = PaletteFrame(self.editor_frame, self.commands)

    def build_commands(self, command_data):
        """ Builds command objects """
        commands = []
        for row in command_data:
            command = Command(*row)
            command.command = getattr(self, command.command)
            if command.shortcut:
                self.root.bind(command.shortcut, lambda e: command.execute())
            commands.append(command)
        return commands

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
        self.root.title("%s - %s" % (file_obj.basename, self.name))

    # methods below are the controller methods

    def open_folder(self, path=None):
        """" open a directory, ask for path if none provided  """
        if not path:
            path = filedialog.askdirectory()
        if path:
            self.model.open_folder(path)

    def preview_file(self, file_obj):
        self.model.set_preview(file_obj)

    def open_file(self, path=None):
        """ open a file, ask for path if none provided  """
        if not path:
            path = filedialog.askopenfilename()
        if path:
            self.model.open_file(path)

    def select_file(self, file_obj, originator):
        """ set a file as selected """
        self.model.set_current_file(file_obj, originator)

    def close_file(self, file_obj=None, originator=None):
        """ close a file """
        if file_obj is None:
            file_obj = self.model.current_file
        self.model.close_file(file_obj, originator)

    def show_welcome(self):
        """ show welcome frame """
        self.editor_frame.show_welcome()

    def show_palette(self, event):
        """ show tool palette """
        self.palette.toggle()
