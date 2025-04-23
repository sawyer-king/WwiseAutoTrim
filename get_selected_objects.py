from pywwise import *
from scipy.io import wavfile


def print_info(info: tuple[WwiseObjectInfo, ...]):
    """
    Print the name, ID, type, and path of a Wwise Object.
    :param info: The `WwiseObjectInfo` containing the information to display.
    """
    for obj in info:
        print(f"Name: {obj.name}")
        print(f"GUID: {obj.guid}")
        print(f"Type: {obj.type}")
        print(f"Path: {obj.path}")
        if obj.type == EObjectType.SOUND:
                samplerate, data = wavfile.read(
                    f"C:/Users/sawya/Documents/WwiseProjects/ToolTesting/Originals/SFX/{obj.name}.wav")
                print(f"Data Type: {data.dtype.name}")
        print()  # Empty line, for formatting purposes.


def main():
    """Set up a callback for object selections in Wwise."""
    ak = new_waapi_connection()
    ak.wwise.ui.selection_changed += print_info


if __name__ == "__main__":
    main()