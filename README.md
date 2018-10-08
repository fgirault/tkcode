# tkcode

Tk Code is a "visual clone" of modern dark themed editors, that shall be considered as a silly tkinter code demo of flat design.

It shows the possibility of building minimal "flat design" user interfaces using tkinter with the ttk module (Themed Tk).

It also implements several common design patterns like command, observer, factory ...

This has been shown at PyCon France 2018. If you're interested in building themes, `tkcode/themes.py` is an exemple of building a ttk.Style() instance and using it. Note that the tkcode theme derives from the _alt__ theme (the parent argument of Style constructor), this minimal base theme may not be available on your platform (only tested on Linux).

The code is not perfect at all : some names are bad, more comments and docstrings would be better ... but it's enough to get started in flat design with tk and ttk.


## Usage

tkcode can by called as a module if available in the PYTHONPATH (or if you're the project directory checkout):

```bash
$ python3 -m tkcode
```

- Open a folder or a file with the link on the welcome page
- Click on a file in the explorer panel to view it
- Double click to make stay in the tabs
- Use Control+P to show the palette, type letters or word and navigate with arrows


## Customize

tkcode static settings are stored in `tkcode/settings.py`. Configurable settings are available at the top of the file so you can customize application name and base colors.


## TODO

For the template goal:

 - i18n (gettext)
 - keyboard shortcuts
 - help screen
 - add feedback when rolling over clickable ui elements (highlight)
 - status bar api
 - image directory loader so usign icons does not requires instantiating PhotoImage

For the editor function (lower priority):

 - save
 - plugin architecture
 - search (there's some async challenge here)
 - syntax highlighter or
 - try to integrate idle3 editing widget ? or fork idle3 to make some silly ux things ?
 - line number

To take over the world:

 - build a framework
