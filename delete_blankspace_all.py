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

    wwise_objects = ak.wwise.core.object.get(query)  # maybe try to get only audio files and not objects ?

    ak.wwise.core.undo.begin_group()

    for obj in wwise_objects:
        if obj.type == EObjectType.SOUND:
            samplerate, data = wavfile.read(f"C:/Users/sawya/Documents/WwiseProjects/ToolTesting/Originals/SFX/{obj.name}.wav")  # obj.path somehow?
            duration = data.shape[0] / samplerate  # not sure that I need this? does duration get used?
            if len(data.shape) == 2:  # idk if this will always return 2 or not?
                channels = 2
            else:
                channels = 1
            num_samples = int(data.size / channels)
            trim_end = num_samples - 1
            trim_begin = 0


            #  FIGURE OUT HOW TO READ (data)
            #  DO I NEED TO CONVERT TO 32 bit to accurately make trim point
            #  if 2 0s in a row then that is the trim point lol
            #  how to use PyWwise to set the trim_begin etc

            prev_sample_value = 0

            #TRIM BEGIN
            for i in range(0, num_samples - 1):
                sample_value = convert_sample(data[i])  # copied garbage

                if (sample_value > 0 and prev_sample_value <= 0) or (sample_value < 0 and prev_sample_value >= 0):
                    trim_begin = i

                prev_sample_value = sample_value

            #TRIM END
            for i in range(num_samples - 1, trim_begin, - 1):
                sample_value = convert_sample(data[i])

                if (sample_value <= 0 and prev_sample_value >= 0) or (sample_value):
                    trim_end = i

                prev_sample_value = sample_value

            obj.trim_begin = trim_begin / samplerate
            obj.trim_end = trim_end / samplerate

            if trim_begin > 0 or trim_end < num_samples - 1:
                temp_dict = {'FileName': obj.name, 'Path': obj.path}
                modified_files_list.append = temp_dict  # make a list of all modified files to be printed in a display to the user

    if len(modified_files_list) > 0:
        print(modified_files_list)  # also think about adding file name + folder path + Wwise actor mixer structure path
    else:
        print("No files were modified.")  # add some display for case where no files were changed

    # Add undo button to each changed file?

    ak.wwise.core.undo.end_group("Set Trim Begin and End points based on empty space In All wav files")  # figure out where this display name is for

    ak.disconnect()


if __name__ == "__main__":
    main()
