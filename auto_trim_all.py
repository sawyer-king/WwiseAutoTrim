# Copyright (c) 2025 Sawyer King. <sawyer.audio@gmail.com>.

from pywwise import *
from scipy.io import wavfile


def main():
    """Check all .wav files in use in the Wwise project for empty space at the beginning or end of the file and
    set trim points to remove that empty space. Also includes the option to add Initial Delay to the sound to keep
    the original sync offset."""
    ak = new_waapi_connection()

    modified_files_list = []

    query = f"$ from type AudioFileSource"

    wwise_objects = ak.wwise.core.object.get(query, (EReturnOptions.ORIGINAL_FILE_PATH,))

    ak.wwise.core.undo.begin_group()

    for obj in wwise_objects:
        samplerate, data = wavfile.read(obj.other[EReturnOptions.ORIGINAL_FILE_PATH])
        channels = data.shape[1]
        num_samples = int(data.size / channels)
        trim_begin_pos = 0
        trim_end_pos = num_samples - 1

        convert_sample = convert_sample_function(data)
        prev_sample_value = 0

        # TRIM BEGIN
        for i in range(0, num_samples - 1):
            sample_value = convert_sample(data[i])

            if (abs(sample_value) > 0 >= abs(prev_sample_value)) or (abs(sample_value) < 0 <= abs(prev_sample_value)):
                trim_begin_pos = i
                break

            prev_sample_value = sample_value

        # TRIM END
        for i in range(num_samples - 1, trim_begin_pos, - 1):
            sample_value = convert_sample(data[i])

            if (abs(sample_value) > 0 >= abs(prev_sample_value)) or (abs(sample_value) < 0 <= abs(prev_sample_value)):
                trim_end_pos = i
                break

            prev_sample_value = sample_value

        trim_begin = trim_begin_pos / samplerate
        trim_end = trim_end_pos / samplerate
        ak.wwise.core.object.set_property(obj.guid, "TrimBegin", trim_begin)
        ak.wwise.core.object.set_property(obj.guid, "TrimEnd", trim_end)

        ak.wwise.core.object.set_property(obj.guid, "FadeInDuration", 0.001)
        ak.wwise.core.object.set_property(obj.guid, "FadeOutDuration", 0.001)

        # INITIAL DELAY
        # sound_parent = ak.wwise.core.object.get(f"$ from object \"{obj.guid}\" select parent")[0]
        # ak.wwise.core.object.set_property(sound_parent.guid, "InitialDelay", trim_begin)

        if trim_begin > 0 or trim_end < num_samples - 1:
            temp_dict = {"FileName": obj.name,
                         "WwiseProjectPath": obj.path,
                         "FolderPath": obj.other[EReturnOptions.ORIGINAL_FILE_PATH]}
            modified_files_list.append(temp_dict)  # make a list of all modified files to be printed in a display to the user

    if len(modified_files_list) > 0:
        print("Modified Files:")
        for file in modified_files_list:
            print(file)
    else:
        print("No files were modified.")

    # Add undo button to each changed file?
    # button for add initial delay to match offset?

    ak.wwise.core.undo.end_group("Auto Trim All")

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
