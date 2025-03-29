# Copyright 2025 Sawyer King

from pywwise import *


def main():
    """Check all .wav files in use in the Wwise project for blank space at the beginning or end of the file and
    remove that blank space.(FIX DOCUSTRING)"""
    ak = new_waapi_connection()

    query = WaqlQuery()
    query.from_project()  # This will  get every object in the Wwise project.

    wwise_objects = ak.wwise.core.object.get(
                    query)  # maybe try to get only audio files and not objects (sound containers?)

    ak.wwise.core.undo.begin_group()

    for obj in wwise_objects:
        if pqweokperoqwk in obj.name:  # If blank space in wav files NEED TO ADD/CHANGE.
            new_file = obj.other  # replace OR EDIT with fixed file

    ak.wwise.core.undo.end_group("Delete Blankspace In All") # figure out where this display name is for

    ak.disconnect()


if __name__ == "__main__":
    main()
