""" visual oriented tools """

import tkinter.ttk

from tkcode.settings import Palette


def build_style(colors: Palette):
    """Create a flat design style based on a palette of colors"""

    style = tkinter.ttk.Style()

    style.theme_create(
        "tkcode",
        parent="default",
        settings={
            ".": {"configure": {"background": colors.bg, "foreground": colors.fg}},
            "TNotebook": {
                "configure": {
                    "tabmargins": [0, 0, 0, 0],
                    "background": colors.bg,
                    "borderwidth": 0,
                }
            },
            "TNotebook.Tab": {
                "configure": {
                    "padding": [8, 12, 18, 12],
                    "background": colors.bg,
                    "foreground": colors.fg,
                    "borderwidth": 0,
                },
                "map": {
                    "background": [
                        ("selected", colors.tab_bg),
                        ("!selected", colors.tab_inactive_bg),
                    ],
                    "foreground": [("selected", colors.tab_fg)],
                    "expand": [("selected", [1, 1, 1, 0])],
                },
            },
            "TPanedwindow": {
                "configure": {"background": colors.tab_bg, "foreground": colors.tab_bg}
            },
            "SideBar.TFrame": {"configure": {"background": colors.sidebar_bg}},
            "SideBar.TButton": {
                "configure": {
                    "background": colors.sidebar_bg,
                    "foreground": colors.sidebar_fg,
                }
            },
            "SidePanel.TFrame": {"configure": {"background": colors.bg}},
            "SidePanel.Label": {
                "configure": {"background": colors.bg, "foreground": colors.fg}
            },
            "SidePanel.Treeview": {
                "configure": {
                    "background": colors.bg,
                    "fieldbackground": colors.bg,
                    "foreground": colors.fg,
                },
                "map": {
                    "background": [("selected", colors.selected_bg)],
                    "foreground": [("selected", colors.selected_fg)],
                },
            },
            "StatusBar.TFrame": {
                "configure": {
                    "background": colors.status_bg,
                    "foreground": colors.status_fg,
                }
            },
            "StatusBar.TLabel": {
                "configure": {
                    "background": colors.status_bg,
                    "foreground": colors.status_fg,
                }
            },
            "Welcome.TFrame": {"configure": {"background": colors.tab_bg}},
            "Heading.TLabel": {
                "configure": {
                    "background": colors.tab_bg,
                    "foreground": colors.tab_fg,
                    "font": ("", 24, ""),
                }
            },
            "SubHeading.TLabel": {
                "configure": {
                    "background": colors.tab_bg,
                    "foreground": colors.fg,
                    "font": ("", 18, ""),
                }
            },
            "Links.TFrame": {
                "configure": {"background": colors.tab_bg, "foreground": colors.fg}
            },
            "Links.TLabel": {
                "configure": {"background": colors.tab_bg, "foreground": colors.fg}
            },
            "Links.TButton": {
                "configure": {"background": colors.tab_bg, "foreground": colors.link}
            },
            "PaletteSelected.TFrame": {
                "configure": {
                    "background": colors.selected_bg,
                    "foreground": colors.selected_fg,
                }
            },
            "PaletteSelected.TLabel": {
                "configure": {
                    "background": colors.selected_bg,
                    "foreground": colors.selected_fg,
                }
            },
        },
    )

    style.layout("Treeview", [("Treeview.treearea", {"sticky": "nswe"})])

    return style
