import tkinter as tk

from pywwise import new_waapi_connection

def main():
    root = tk.Tk()

    def execute():
        if entry.get() == "":
            quit(-1)
        ak = new_waapi_connection()
        objs = ak.wwise.ui.get_selected_objects()
        for obj in objs:
            ak.wwise.core.object.set_name(obj.guid, f"{entry.get()}_{obj.name}")

    label = tk.Label(root, text="Prefix")
    label.pack()

    entry = tk.Entry(root)
    entry.pack()

    button = tk.Button(root, text="Confirm", command=execute)
    button.pack()

    root.mainloop()


if __name__ == "__main__":
    main()