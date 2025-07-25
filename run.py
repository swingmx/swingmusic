# Launcher script
import swingmusic.__main__ as app
import multiprocessing

if __name__ == "__main__":
    # add freeze support here as pyinstaller uses this entry only
    multiprocessing.freeze_support()
    app.run()
