"""Application commands implemented as decorated functions"""

import gettext
from gettext import gettext as _

# may be rewrite the filedialog one day
import tkinter.filedialog

# function decorator to register command
from tkcode.commander import command


@command(title=_("Show Welcome"), description=_("Show welcome screen"))
def show_welcome(app):
    """ show welcome frame """
    app.editor_frame.show_welcome()


@command(
    title=_("Open file"),
    category=_("FILE"),
    description=_("Open file from filesystem"),
    shortcut=_("<Control-o>"),
)
def open_file(self, path=None):
    """ open a file, ask for path if none provided  """
    if not path:
        path = tkinter.filedialog.askopenfilename()
    if path:
        self.model.open_file(path)


@command(
    title=_("Open folder"),
    category=_("FILE"),
    description=_("Open folder from filesystem"),
    shortcut=_("<Control-Shift-o>"),
)
def open_folder(app, path=None):
    """" open a directory, ask for path if none provided  """
    if not path:
        path = tkinter.filedialog.askdirectory()
    if path:
        app.model.open_folder(path)


@command(
    title=_("Close file"),
    category=_("FILE"),
    description=_("Close file"),
    shortcut=_("<Control-W>"),
)
def close_file(app, file_obj=None, originator=None):
    """ close a file """
    if file_obj is None:
        file_obj = app.model.current_file
    app.model.close_file(file_obj, originator)
