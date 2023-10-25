import tkinter as tk
import functions as fc
from functools import partial
from crops import crop_class_dict as ccd

# THIS FILE IS REALLY BAD OK DONT LOOK AT IT


class VariableStoring:
    def __init__(self):
        self.crop_variable = None


storage = VariableStoring()


def create_gui(driver):
    # Create the main window
    window = tk.Tk()
    window.title("Simple GUI")

    bt_height = 12
    bt_width = 25
    font = ("Helvetica", 14)
    # Create buttons and place them in a 2x2 grid
    button1 = tk.Button(window, text="Harvest Crops", height=bt_height, width=bt_width, font=font,
                        command=partial(fc.harvest, driver), bg="light green")
    button2 = tk.Button(window, text="Plant Crops", height=bt_height, width=bt_width, font=font,
                        command=partial(get_crop_name_and_plant, driver), bg='#D2B48C')
    button3 = tk.Button(window, text="Water Crops", height=bt_height, width=bt_width, font=font,
                        command=partial(fc.water_crops, driver), bg="light blue")
    button4 = tk.Button(window, text="Button 4", height=bt_height, width=bt_width, font=font)

    button1.grid(row=0, column=0)
    button2.grid(row=0, column=1)
    button3.grid(row=1, column=0)
    button4.grid(row=1, column=1)

    # Start the GUI event loop
    window.mainloop()


def crop_input():
    new_window = tk.Toplevel()
    new_window.title("Crop Input")
    new_window.geometry("300x270")
    new_window.configure(bg="#D2B48C")

    label = tk.Label(new_window, text="Crop to plant:", font=("Helvetica", 14), bg="#D2B48C")
    label.pack(pady = 8)  # Add padding between label and input box

    crops = fc.get_supported_crops(ccd)

    label2 = tk.Label(new_window,
                      text=f"Crops accepted: {crops}",
                      font=("Helvetica", 11), bg="#D2B48C", wraplength=200)
    label2.pack()

    label3 = tk.Label(new_window, text="dont type nonsense in (will either do nothing or use last selected crop)", font=("Helvetica", 8), bg="#D2B48C", wraplength=200)
    label3.pack()

    input_box = tk.Entry(new_window, font=("Helvetica", 15))
    input_box.pack(pady=8)  # Add padding between input box and button

    def store_input():
        crop = input_box.get()
        storage.crop_variable = crop
        new_window.destroy()
        new_window.quit()

    submit_button = tk.Button(new_window, text="Submit", command=store_input, font=("Helvetica", 12), bg="#CD853F")
    submit_button.pack(pady=10)  # Add padding below the button

    new_window.mainloop()


def get_crop_name_and_plant(driver):
    crop_input()
    crop_name = storage.crop_variable
    print(crop_name)
    if crop_name:
        fc.plant(crop_name, driver)
