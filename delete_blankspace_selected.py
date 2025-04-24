# Copyright 2025 Sawyer King

from pywwise import *


def main():
    """Check selected .wav files in use in the Wwise project for empty space at the beginning or end of the file and
    set trim points to remove that empty space. Also includes a GUI component that gives the option to add
    Initial Delay to the sound to keep the original sync offset."""
    ak = new_waapi_connection()

    # idk if this stuff is right but
    selected = ak.wwise.ui.getSelectedObjects
    for obj in selected:
        awdawd

    # stuff goes here.

    ak.wwise.core.undo.end_group("Delete Blankspace In Selected wav files")

    ak.disconnect()


if __name__ == "__main__":
    main()
