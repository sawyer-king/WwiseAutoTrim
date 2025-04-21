# Copyright 2025 Sawyer King

from pywwise import *
from scipy.io import wavfile


def main():
    """Check all .wav files in use in the Wwise project for blank space at the beginning or end of the file and
    remove that blank space.(FIX DOCUSTRING)"""
    ak = new_waapi_connection()

    modified_files_list = []  # may give error idk if i have to declare this as a list of dictionaries?

    query = WaqlQuery()
    query.from_project()  # This will  get every object in the Wwise project.

    wwise_objects = ak.wwise.core.object.get(
        query)  # maybe try to get only audio files and not objects (sound containers?)

    ak.wwise.core.undo.begin_group()

    for obj in wwise_objects:
        if obj.type == EObjectType.SOUND:
            print("its a sound!")
            samplerate, data = wavfile.read(f"C:/Users/sawya/Documents/WwiseProjects/ToolTesting/Originals/SFX/{obj.name}.wav")  # obj.path somehow?
            duration = data.shape[0] / samplerate
            print(duration)
            print(data)

            '''
            AudioSource.trim_begin = trim_begin
            AudioSource.trim_end = trim_end

            if trim_begin > 0 or trim_end > 0:
                temp_dict = {'FileName':obj.name, 'Path':obj.path}
                modified_files_list.append = temp_dict #make a list of all modified files to be printed in a display to the user
            '''

    if len(modified_files_list) > 0:
        print(modified_files_list)  # also think about adding file name + folder path + Wwise actor mixer structure path
    else:
        print("No files were modified.")  # add some display for case where no files were changed

    ak.wwise.core.undo.end_group("Delete Blankspace In All wav files")  # figure out where this display name is for

    ak.disconnect()


if __name__ == "__main__":
    main()
