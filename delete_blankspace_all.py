# Copyright 2025 Sawyer King
import wave
import audioop

from pywwise import *


def main():
    """Check all .wav files in use in the Wwise project for blank space at the beginning or end of the file and
    remove that blank space.(FIX DOCUSTRING)"""
    ak = new_waapi_connection()

    modified_files_list = [] #may give error idk if i have to declare this as a list of dictionaries? or if python knows

    query = WaqlQuery()
    query.from_project()  # This will  get every object in the Wwise project.

    wwise_objects = ak.wwise.core.object.get(
                    query)  # maybe try to get only audio files and not objects (sound containers?)

    ak.wwise.core.undo.begin_group()

    for obj in wwise_objects:
        if obj.type == Sound:
            if oiawjd in obj.name:
                old_bit_depth = wavFile.getsampwidth() #returns value of 1-4 (x8 for bit depth if needed) need to get bit depth before I can change it using lin2lin

                wav = wave.open("piano2.wav") #https://stackoverflow.com/questions/27895186/what-type-of-file-is-the-sound-fragment-parameter-for-audioop
                print(audioop.avg(wav.readframes(wav.getnframes()), wav.getsampwidth()))
                wav.rewind()
                print(audioop.max(wav.readframes(wav.getnframes()), wav.getsampwidth()))
                #wav = wave.open("piano2.wav")
                #string_wav = wav.readframes(wav.getnframes())
                #print(audioop.avg(string_wav, wav.getsampwidth()))
                # wav.rewind()
                #print(audioop.max(string_wav, wav.getsampwidth()))

                if old_bit_depth > 1:
                    new_frames = audioop.lin2lin(frames, old_bit_depth, 4)  # If blank space in wav files NEED TO ADD/CHANGE. https://stackoverflow.com/questions/44812553/how-to-convert-a-24-bit-wav-file-to-16-or-32-bit-files-in-python3
                else:
                    new_frames = audioop.lin2lin(frames, old_bit_depth, 4) # If blank space in wav files NEED TO ADD/CHANGE. https://stackoverflow.com/questions/44812553/how-to-convert-a-24-bit-wav-file-to-16-or-32-bit-files-in-python3
                    new_frames = audioop.bias(new_frames, 4, 128)#this 128 may only be needed when converting 8bit files idk here is the docs: https://docs.python.org/3.10/library/audioop.html

                new_file = obj.other  # replace OR EDIT with fixed file

                temp_dict = {'FileName':new_file, 'Path':obj.path}
                modified_files_list.append = temp_dict #make a list of all modified files to be printed in a display to the user

    if len(modified_files_list) > 0:
        print(modified_files_list) # also think about adding file name + folder path + Wwise actor mixer structure path
    else:
        print("No files were modified.") #add some display for case where no files were changed

    ak.wwise.core.undo.end_group("Delete Blankspace In All wav files") # figure out where this display name is for

    ak.disconnect()


if __name__ == "__main__":
    main()
