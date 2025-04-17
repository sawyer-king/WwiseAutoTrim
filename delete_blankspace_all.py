# Copyright 2025 Sawyer King
import audioop

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
        if obj.type == Sound:
            if oiawjd in obj.name:
                old_bit_depth = wavFile.getsampwidth() #returns value of 1-4 (x8 for bit depth if needed) need to get bit depth before I can change it using lin2lin
                new_frames = audioop.lin2lin(frames, old_bit_depth, 4) # If blank space in wav files NEED TO ADD/CHANGE. https://stackoverflow.com/questions/44812553/how-to-convert-a-24-bit-wav-file-to-16-or-32-bit-files-in-python3
                new_frames = audioop.bias(new_frames, 4, 128)#this 128 may only be needed when converting 8bit files idk here is the docs: https://docs.python.org/3.10/library/audioop.html

                new_file = obj.other  # replace OR EDIT with fixed file

    ak.wwise.core.undo.end_group("Delete Blankspace In All wav files") # figure out where this display name is for

    ak.disconnect()


if __name__ == "__main__":
    main()
