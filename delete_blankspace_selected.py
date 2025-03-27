# Copyright 2025 Sawyer King

from pywwise import *


def main():
    """Check selected .wav files the Wwise project for blank space at the beginning or end of the file and
        remove that blank space."""
    ak = new_waapi_connection()

    # stuff goes here.

    ak.wwise.core.undo.end_group("Delete Blankspace In Selected")

    ak.disconnect()


if __name__ == "__main__":
    main()
