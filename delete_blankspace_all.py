# Copyright 2025 Sawyer King

from pywwise import *
from scipy.io import wavfile


def main():
    """Check all .wav files in use in the Wwise project for blank space at the beginning or end of the file and
    set trim points to remove that blank space.(FIX DOCUSTRING)"""
    ak = new_waapi_connection()

    modified_files_list = []  # may give error idk if i have to declare this as a list of dictionaries?

    query = WaqlQuery() # maybe WaqlQuery().from_project().where("type = 'Sound'") ?????  see below
    query.from_project()  # This will  get every object in the Wwise project. see above

    wwise_objects = ak.wwise.core.object.get(query)  # maybe try to get only audio files and not objects ? see line 12
    # wwise_objects = ak.wwise.core.object.get(query, EReturnOptions.FILE_PATH)   IDK if this will be the solution

    ak.wwise.core.undo.begin_group()

    for obj in wwise_objects:
        if obj.type == EObjectType.SOUND:
            # obj.other[EReturnOptions.FILE_PATH] OR  file_path = obj.other.get(EReturnOptions.FILE_PATH) ?????
            samplerate, data = wavfile.read(f"C:/Users/sawya/Documents/WwiseProjects/ToolTesting/Originals/SFX/{obj.name}.wav")  # obj.path somehow?
            duration = data.shape[0] / samplerate  # not sure that I need this? does duration get used?
            if len(data.shape) == 2:  # idk if this will always return 2 or not? might need more funcitonality than just 2 channel ie 5.1, 7.1 files
                channels = 2
            else:
                channels = 1
            # len(data.shape) = channels    #  Can I not just do this lol?
            num_samples = int(data.size / channels)
            trim_end = num_samples - 1
            trim_begin = 0

            convert_sample = convert_sample_function(data)
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

                if (sample_value > 0 and prev_sample_value <= 0) or (sample_value < 0 and prev_sample_value >= 0):
                    trim_end = i

                prev_sample_value = sample_value

            obj.trim_begin = trim_begin / samplerate
            obj.trim_end = trim_end / samplerate

            obj.fade_in_duration = 0.01  # im not sure what these values should be, probably the default OR very small fade?
            obj.fade_out_duration = 0.01

            # obj.initial_delay = trim_begin / sample_rate    # can add initial delay to keep same sync if you want? maybe add a button for this like revert trims?

            if trim_begin > 0 or trim_end < num_samples - 1:
                temp_dict = {'FileName': obj.name, 'Path': obj.path}
                modified_files_list.append(temp_dict)  # make a list of all modified files to be printed in a display to the user

    if len(modified_files_list) > 0:
        print("Modified Files:")
        for file in modified_files_list:
            print(file)  # also think about adding file name + folder path + Wwise actor mixer structure path
    else:
        print("No files were modified.")  # add some display for case where no files were changed

    # Add undo button to each changed file?
    # button for add initial delay to match offset? added line above in if statement

    ak.wwise.core.undo.end_group("Set Trim Begin and End points based on empty space In All wav files")  # figure out where this display name is for

    ak.disconnect()


def convert_sample_function(sample):
    converted_sample = convert_sample_functions[sample.dtype.name]
    if len(sample.shape) == 1:  # conversion for mono files
        return converted_sample
    return lambda a: converted_sample(a.max())  # conversion for any channel count other than mono


convert_sample_functions = {
    "int16": lambda x: x / 32767,
    "int32": lambda x: x / 2147483647,
    "float32": lambda x: x
}


if __name__ == "__main__":
    main()
