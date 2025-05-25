# Launcher script

import multiprocessing
import swingmusic.__main__ as app

if __name__ == "__main__":
    multiprocessing.freeze_support()
    multiprocessing.set_start_method("spawn")
    app.run()
