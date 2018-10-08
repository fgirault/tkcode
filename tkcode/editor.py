"""editor tools"""
import tkinter as tk

from tkcode.settings import COLORS
from tkcode.welcome import WelcomeTab

# pylint: disable=too-many-ancestors


class EditorFrame(tk.ttk.Frame):
    """ A container for the notebook, including bottom console """

    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

        app.model.add_observer(self)

        self.notebook = tk.ttk.Notebook(self)

        self.notebook.pack(fill=tk.BOTH, expand=tk.YES)

        self.path2id = {}
        self.id2path = {}

        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_changed)

        self.welcome_id = None

        self.preview = TextEditorFrame(self)

    def show_welcome(self):
        """ show a welcome tab at the first notebook position """
        if not self.welcome_id:
            if self.notebook.index("end"):
                self.notebook.insert(0, WelcomeTab(self, self.app), text="Welcome")
            else:
                self.notebook.add(WelcomeTab(self, self.app), text="Welcome")
            self.welcome_id = self.notebook.tabs()[0]

        self.notebook.select(self.welcome_id)

    def on_file_preview(self, file_obj):
        """preview a file : select if opened, or open a temporary tab"""
        if file_obj in self.id2path.values():
            self.on_file_selected(file_obj)
            return

        self.preview.set_file_obj(file_obj)

        tab_id = self.notebook.select()

        if tab_id:
            pos = self.notebook.index(tab_id)

            pos = pos + 1

            if not pos < self.notebook.index("end"):
                pos = "end"

            tab_id = self.notebook.insert(pos, self.preview, text=file_obj.basename)

            if pos == "end":
                pos = -1

            self.notebook.select(self.notebook.tabs()[pos])
        else:
            self.notebook.add(self.preview, text=file_obj.basename)
            self.notebook.select(self.notebook.tabs()[-1])

    def on_file_open(self, file_obj):
        """open the file object in a tab """
        # check if not already opened
        if file_obj in self.id2path.values():
            self.on_file_selected(file_obj)
            return

        # create a new editor
        editor = TextEditorFrame(self.notebook, file_obj)
        tab_id = self.notebook.select()

        if tab_id:
            pos = self.notebook.index(tab_id)

            pos = pos + 1
            if not pos < self.notebook.index("end"):
                pos = "end"
            self.notebook.insert(pos, editor, text=file_obj.basename)

            if pos == "end":
                pos = -1
            tab_id = self.notebook.tabs()[pos]
        else:
            self.notebook.add(editor, text=file_obj.basename)
            tab_id = self.notebook.tabs()[-1]

        # fill cache and indices
        self.path2id[file_obj.path] = tab_id
        self.id2path[tab_id] = file_obj

        self.notebook.select(tab_id)

        if file_obj is self.preview.file_obj:
            self.notebook.hide(self.preview)

    def on_file_selected(self, file_obj):
        """select an opened file"""
        tab_id = self.notebook.select()
        if tab_id not in self.id2path or self.id2path[tab_id] is not file_obj:
            self.notebook.select(self.path2id[file_obj.path])

    def on_file_closed(self, file_obj):
        """remove the tab associated with the file object"""
        if file_obj is self.preview.file_obj:
            self.notebook.hide(self.preview)
            return
        tab_id = self.path2id[file_obj.path]
        self.notebook.forget(tab_id)
        del self.path2id[file_obj.path]
        del self.id2path[tab_id]

    def on_tab_changed(self, event):
        """tell the model the current file has changed"""
        tab_id = self.notebook.select()
        if tab_id in self.id2path:
            self.app.select_file(self.id2path[tab_id], self)


class TextEditorFrame(tk.ttk.Frame):
    """ A frame that contains a text editor """

    def __init__(self, parent, file_obj=None):
        super().__init__(parent)
        self.text = tk.Text(
            self,
            background=COLORS.text_bg,
            foreground="#eeeeee",
            insertbackground="#eeeeee",
            borderwidth=0,
            highlightthickness=0,
            relief=tk.FLAT,
            takefocus=0,
        )
        self.text.pack(expand=tk.YES, fill=tk.BOTH)
        self.set_file_obj(file_obj)

    def set_file_obj(self, file_obj):
        self.file_obj = file_obj
        if file_obj:
            self.text.delete("0.0", tk.END)
            self.text.insert(tk.END, file_obj.content)
