# Launcher script
import sys
import zipfile
import multiprocessing
from pathlib import Path
import swingmusic.__main__ as app

if __name__ == "__main__":
	# Fixed: freeze_support() must be called immediately to prevent 
	# recursive process spawning and ArgumentParser errors on Windows EXE.
    multiprocessing.freeze_support()
    
    # this entry should only be used by pyinstaller.
    # add freeze support here as pyinstaller uses this entry

    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        # INFO: extract client.zip to sys._MEIPASS
        with zipfile.ZipFile(sys._MEIPASS + "/client.zip", "r") as zip_ref:
            zip_ref.extractall(sys._MEIPASS)

        client = Path(sys._MEIPASS) / "client"
        client_str = str(client)

        sys.argv.extend(["--client", client_str])
        sys.orig_argv.extend(["--client", client_str])

    app.run()
