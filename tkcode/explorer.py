""" tk.explorer contains a side panel class to explore filesystems """
import os

import tkinter as tk
from tkinter import ttk

from .sidepanel import SidePanel


class Explorer(SidePanel):
    """" A side panel showing project file system """

    TITLE = "EXPLORER"

    ICON_PATH = "explorer_inactive.png"

    def __init__(self, parent, app):
        super().__init__(parent)

        self.open_dict = {}
        self.expl_dict = {}
        self.path2id = {}

        self.dir_dict = {}

        self.app = app

        self.current_iid = ""
        self.curexpl_iid = ""

        app.model.add_observer(self)

        container = ttk.Frame(self)
        container.pack(fill="both", expand=True)

        self.tree = ttk.Treeview(
            columns=(0,), show="tree", style="SidePanel.Treeview", selectmode="none"
        )

        # scrollbars will come later
        # vsb = ttk.Scrollbar(orient="vertical", command=self.tree.yview)
        # hsb = ttk.Scrollbar(orient="horizontal", command=self.tree.xview)

        # self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        self.tree.grid(column=0, row=0, sticky="nsew", in_=container)
        # vsb.grid(column=1, row=0, sticky='ns', in_=container)
        # hsb.grid(column=0, row=1, sticky='ew', in_=container)

        container.grid_columnconfigure(0, weight=1)
        container.grid_rowconfigure(0, weight=1)

        # Hide column
        self.tree.column(0, stretch=tk.NO, width=0, minwidth=0)

        # Fixed items
        self.openfiles_item = self.tree.insert(
            "", "end", text="OPEN FILES", open=tk.YES, tags=("expandable",)
        )

        self.folders_item = self.tree.insert(
            "", "end", text="FOLDERS", open=tk.YES, tags=("expandable",)
        )


        self.tree.bind("<<TreeviewOpen>>", self.on_treeview_open)
        # "<<TreeviewSelect>>" handling is rewritten in on_click
        self.tree.bind("<Button-1>", self.on_click)
        self.tree.bind("<Double-Button-1>", self.on_doubleclick)

        self.populate()

    def populate(self):
        """ Populate the explorer based on data model """
        for file_obj in self.app.model.openfiles:
            self.add_to_openfiles(file_obj)

        for folder in self.app.model.folders:
            self.add_to_folders(folder)

    def add_to_openfiles(self, file_obj):
        iid = self.tree.insert(
            self.openfiles_item,
            "end",
            text=file_obj.basename,
            values=(file_obj.path,),  # iid=file_obj.path,
            tags=("file", "openfiles", "selectable"),
        )
        self.open_dict[file_obj.path] = file_obj
        self.path2id[file_obj.path] = iid

    def add_to_folders(self, folder):
        iid = self.tree.insert(
            self.folders_item,
            "end",
            text=folder.basename,
            open=tk.YES,
            values=(folder.path,),
            tags=("dir", "expandable"),
        )
        self.dir_dict[folder.path] = iid
        self.populate_folder(iid, folder)
        return iid

    def on_treeview_open(self, event):
        sel = self.tree.focus()

    def on_folder_open(self, folder):
        if folder.path not in self.dir_dict:
            iid = self.add_to_folders(folder)
            self.tree.see(iid)

    def populate_folder(self, iid, folder):
        for child in folder.entries:
            if hasattr(child, "entries"):
                f_iid = self.tree.insert(
                    iid,
                    "end",
                    text=child.basename,
                    values=(child.path,),
                    tags=("dir", "expandable"),
                )
                self.populate_folder(f_iid, child)
            else:
                f_iid = self.tree.insert(
                    iid,
                    "end",
                    text=child.basename,
                    values=(child.path,),
                    tags=("file", "selectable"),
                )
                self.expl_dict[child.path] = f_iid

    def selection_set(self):
        self.tree.selection_set(
            [item for item in (self.current_iid, self.curexpl_iid) if item]
        )

    def on_file_open(self, file_obj):
        if file_obj not in self.open_dict.values():
            self.add_to_openfiles(file_obj)
        else:
            self.on_file_selected(file_obj)

    def on_file_selected(self, file_obj):
        if file_obj.path in self.path2id:
            iid = self.path2id[file_obj.path]
            self.tree.focus(iid)
            self.current_iid = iid
        else:
            self.current_iid = None

        if file_obj.path in self.expl_dict:
            self.curexpl_iid = self.expl_dict[file_obj.path]
        else:
            self.curexpl_iid = None

        self.selection_set()

    def on_file_closed(self, file_obj):
        iid = self.path2id[file_obj.path]
        del self.path2id[file_obj.path]
        if self.current_iid == iid:
            self.current_iid = None

        if file_obj.path in self.expl_dict:
            f_iid = self.expl_dict[file_obj.path]
            if self.curexpl_iid == f_iid:
                self.curexpl_iid = None
        if file_obj.path in self.open_dict:
            del self.open_dict[file_obj.path]
        self.tree.delete(iid)

    def on_click(self, event):
        """ callback on clicking tree widget """
        tree = event.widget
        iid = tree.identify_row(event.y)
        if iid:

            tags = tree.item(iid, "tags")

            if "file" in tags:
                path = self.tree.item(iid)["values"][0]

                if "openfiles" in tags:
                    self.current_iid = iid
                    file_obj = self.open_dict[path]
                    if path in self.expl_dict:
                        self.curexpl_iid = iid
                    self.app.select_file(file_obj, self)

                else:
                    self.curexpl_iid = iid
                    self.app.preview_file(path)

                if "selectable" in tags:
                    self.selection_set()

            if "expandable" in tags:
                # toggle open state
                tree.item(iid, open=not tree.item(iid, "open"))

        # do not propagate event, or folder will open then close is expand icon
        # is clicked
        return "break"

    def on_doubleclick(self, event):
        # open
        tree = event.widget
        iid = tree.identify_row(event.y)
        if iid:
            tags = tree.item(iid, "tags")

            if "file" in tags:
                path = self.tree.item(iid)["values"][0]

                if "openfiles" in tags:
                    self.current_iid = iid
                    file_obj = self.open_dict[path]
                    if path in self.expl_dict:
                        self.curexpl_iid = iid
                    self.app.select_file(file_obj, self)
                else:
                    self.curexpl_iid = iid
                    self.app.open_file(path)

        return "break"
