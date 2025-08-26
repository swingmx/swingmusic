# Launcher script
import swingmusic.__main__ as app
import sys
import multiprocessing

if __name__ == "__main__":
    # this entry should only be used by pyinstaller.
    # add freeze support here as pyinstaller uses this entry only

    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        client = sys._MEIPASS + "/client"
        sys.argv.extend(["--fallback-client", client])
        sys.orig_argv.extend(["--fallback-client", client])

    multiprocessing.freeze_support()
    app.run()
