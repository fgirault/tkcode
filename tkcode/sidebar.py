""" a microframework for building sidebar with buttons to switch panel """
import os
import tkinter as tk
from tkinter import ttk

from tkcode.explorer import Explorer
from tkcode.search import Search

from tkcode.settings import IMG_DIR

# pylint: disable=too-many-ancestors

class ActivityButton(ttk.Button):
    """A button of the side bar, toggle the visibility of the panel content """
    def __init__(self, parent, panel_class, **kw):
        self.panel_class = panel_class
        self.icon_img = tk.PhotoImage(file=os.path.join(IMG_DIR, panel_class.ICON_PATH))
        super().__init__(parent, image=self.icon_img, style="SideBar.TButton", **kw)


class ButtonStack(ttk.Frame):
    """ the left side frame containing buttons to show or hide panels in side bars """

    def __init__(self, parent, app, panel_classes):
        super().__init__(parent, style="SideBar.TFrame")
        self.buttons = []
        for panel_class in panel_classes:
            button = ActivityButton(
                self, panel_class, command=parent.build_panel_callback(panel_class)
            )
            button.pack(side=tk.TOP, padx=4, pady=4)
            self.buttons.append(button)
        ttk.Button(self, text="?", command=app.show_welcome).pack(
            side=tk.BOTTOM, padx=4, pady=4
        )


class SideBar(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, style="SideBar.TFrame")
        self.app = app
        self.paned = parent
        self.button_stack = ButtonStack(self, app, [Explorer, Search])
        self.button_stack.pack(side=tk.LEFT, anchor=tk.N)
        self.panels = {}
        self.current_panel = None
        self.sashpos = None
        self.minwidth = None

        app.model.add_observer(self)

    def build_panel_callback(self, class_obj):
        """ create a callback for sidebar button clicks """
        class_name = class_obj.__name__

        def panel_callback():
            """a callback for sidebar buttons"""
            if self.minwidth is None:
                self.minwidth = self.button_stack.winfo_width()

            if self.current_panel:
                self.sashpos = self.paned.sashpos(0)
                self.current_panel.forget()
                if isinstance(self.current_panel, class_obj):
                    self.current_panel = None
                    self.paned.sashpos(0, self.minwidth)
                    return

            if class_obj.__name__ in self.panels:
                panel = self.panels[class_name]
            else:
                panel = self.panels[class_name] = class_obj(self, self.app)

            panel.pack(side=tk.LEFT, expand=1, fill=tk.BOTH)

            if self.sashpos is None:
                self.sashpos = 300

            self.paned.sashpos(0, self.sashpos)

            self.current_panel = panel

        return panel_callback

    def on_folder_open(self, folder):
        """model callback"""
        if not isinstance(self.current_panel, Explorer):
            self.button_stack.buttons[0].invoke()
