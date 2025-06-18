__author__ = "Eliot Christon"
__email__  = "eliot.christon@gmail.com"
__github__ = "eliot-christon"

"""
This file contains the main UI of the application.
I will use the tkinter library to create the UI.

The UI will have the following components:
- A text box to input the notes.
- A round selector to select the instrument.
- A button to submit.

The output position is displayed in the left side of the window.
Depending on the instrument, this side will represent the neck of it, with the corresponding number of strings and frets.
The position will be displayed as a red dot on the neck.
"""

import tkinter as tk
from tkinter import messagebox, ttk, StringVar, IntVar, END
from typing import List
from requests import post, get

URL = "http://localhost:8000/"


class MainUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Position Finder")
        self.window.geometry("800x600")
        self.notes = tk.Text(self.window, height=1, width=30)
        self.notes.pack(pady=10)
        self.instrument = StringVar()
        self.instrument.set("Guitar")
        self.all_instruments = {"Guitar" : 6, "Bass" : 4, "Ukulele" : 4}
        self.instrument_selector = ttk.Combobox(self.window, textvariable=self.instrument, values=list(self.all_instruments.keys()))
        self.submit = tk.Button(self.window, text="Submit", command=self.submit)
        self.submit.pack(pady=10)
        self.position = tk.Canvas(self.window, bg="white", width=400, height=400)
        self.position.pack(side=tk.LEFT, padx=10)
        self.window.mainloop()
    
    def draw_neck(self):
        # depending on the number of strings
        for s in range(self.all_instruments[self.instrument.get()]):
            # draw the strings
            self.position.create_line(10, 10 + 50 * s, 390, 10 + 50 * s)
            # depending on the number of frets
            for f in range(5):
                # draw the frets
                self.position.create_line(10 + 80 * f, 10 + 50 * s, 10 + 80 * f, 60 + 50 * s)

    def submit(self):
        notes = self.notes.get("1.0", END).strip().split()
        instrument = self.instrument.get()
        if len(notes) == 0:
            messagebox.showerror("Error", "Please enter some notes.")
            return
        if instrument == "Guitar":
            instrument = "Guitar"
        else:
            messagebox.showerror("Error", "Instrument not found.")
            return

        response = post(URL + "getPosFromNotes", json={
            "notes": notes,
            "instrument": instrument
        }, headers={"Content-Type": "application/json"})
        
        if response.status_code == 200:
            position = response.json()
            print(position)
            self.display_position(position)
        else:
            messagebox.showerror(str(response.status_code), response.text)


if __name__ == "__main__":
    MainUI()