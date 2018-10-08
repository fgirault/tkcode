import sys
import os

from tkcode.app import App

# TODO arg parsing

app = App()

# For development only, until state recovery comes :)
app.build_ui()

if len(sys.argv) > 1:
    arg = sys.argv[-1]
    if os.path.isdir(arg):
        app.open_folder(arg)
    else:
        app.open_file(arg)
else:
    # TODO add condition depending on settings
    app.show_welcome()

app.run()
