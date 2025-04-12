#iJ

from tkinter import ttk
import tkinter as tk

root = tk.Tk()
root.title('Scaler') ## DO ZMIANY

window_size = [1045, 385] 

root.geometry(f"{window_size[0]}x{window_size[1]}")

def window_size_update(window_size):
    root.geometry(f"{window_size[0]}x{window_size[1]}")
default_strings = 6
default_frets = 22


notes = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

scales = {
    "Major": [2,2,1,2,2,2,1],
    "Minor":[2,1,2,2,1,2,2]}

default_tuning = ["E", "A", "D", "G", "B", "E"]
fretboard = []
tuning = []
current_tuning = []
new_tuning = []
previous_note = []
default = 0

def trace_callback(*args):
    window_size_x = (50 + int(frets_entry.get())*45)
    window_size_y =(110 + int(strings_entry.get())*45)

    if window_size_x < 335:
        window_size_x = 335

    window_size = [window_size_x, window_size_y]
    window_size_update(window_size)

    global default

    def trace_tuning(*args, entry_id):
        global default
        previous_note.clear()

        current_tuning = []
        current_scale = []
        current_tuning = [string_var.get() for string_var in tuning]
        fret_x = 50
        fret_y = 110
        loops = 0
        f = 0

        if note_combo.get() != "" and scale_combo.get() != "":
            scale_note = notes.index(note_combo.get())
            y = scale_note

            for i in scales[scale_combo.get()]:
                y = y + i
                if y > 11:
                    y = (y - 12)
                try:
                    current_scale.append(notes[y])
                except:
                    continue

        for strings in range(int(strings_entry.get())):
            u = notes.index(current_tuning[strings])
            loops = 0

            for frets in range(int(frets_entry.get())):
                text_box = tk.Text(root)
                u = u + 1
                
                if u > 11:
                    u = (u - 12)

                if loops == 0:
                    previous_note.append(notes[u])
                
                if previous_note[f] in current_scale:
                    text_box.configure(fg = "red")
                else:
                    text_box.configure(fg = "black")

                text_box.insert(tk.END, previous_note[f])
                f = f + 1

                text_box.place(x=fret_x,y=fret_y, width=40, height=40)
                fret_x = fret_x + 45

                fretboard.append(text_box)

            loops = loops + 1
            fret_y = fret_y + 45
            fret_x = 50

        new_tuning.clear()
        new_tuning.extend(current_tuning)
        previous_note.clear()
        default = 1
        
    if len(strings_entry.get()) > 2: trace_strings.set(strings_entry.get()[:2]);return
    if len(frets_entry.get()) > 2: trace_frets.set(frets_entry.get()[:2]);return

    for i in fretboard:
        try:
            i.destroy()
        except:
            fretboard.clear()
            tuning.clear()

    fret_numbers_x = 5
    string_y = 110

    for fret_numbers in range(int(frets_entry.get())+1):
        text_box = tk.Text(root)
        text_box.insert(tk.END, str(fret_numbers))
        text_box.place(x=fret_numbers_x,y=65, width=40, height=40)
        fret_numbers_x = fret_numbers_x + 45
        fretboard.append(text_box)

    tuning.clear()

    for strings in range(int(strings_entry.get())):
        string_entry_var = tk.StringVar()
        tuning.append(string_entry_var)
        string_entry = tk.Entry(root, textvar=string_entry_var)
        fretboard.append(string_entry)
        string_entry.place(x=5,y=string_y, width=40, height=40)
        string_entry_var.trace("w", lambda *args, entry_id=strings: trace_tuning(*args, entry_id=entry_id))
        
        #default = 0
        if default == 0:
            try:
                while True:
                    try:
                        string_entry.insert(0, default_tuning[int(strings)])
                    except:
                        continue
                    else:
                        default_tuning.extend("E")
                        break
            except:
                pass

        #default != 0 
        else:
            try:
                string_entry.insert(0, current_tuning[int(strings)])
            except:
                while True:
                    try:
                        string_entry.insert(0, new_tuning[int(strings)])
                    except:
                        continue
                    else:
                        new_tuning.extend("E")
                        break
        try:
            trace_tuning(*args, entry_id=strings)
        except:
            pass

        string_y = string_y + 45

trace_scale = tk.StringVar()
trace_scale.trace('w', trace_callback)
trace_note = tk.StringVar()
trace_note.trace('w', trace_callback)
trace_strings = tk.StringVar()
trace_strings.trace('w', trace_callback)
trace_frets = tk.StringVar()
trace_frets.trace('w', trace_callback)

scale_label = tk.Label(root, text="Scale", font=("Halvetica", 12), justify="left")
scale_label.place(x=5, y=5)

note_label = tk.Label(root, text="Note", font=("Helvetica", 12), justify="left")
note_label.place(x=5, y=35)

scale_combo = ttk.Combobox(state="readonly", values=["Major", "Minor"], textvar=trace_scale)
scale_combo.place(x=55, y=5, width=150, height=25)

note_combo = ttk.Combobox(state="readonly", values=["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"], textvar=trace_note)
note_combo.place(x=55, y=35, width=50, height=25)

strings_label = tk.Label(root, text="Strings", font=("Halvetica", 12), justify="left")
strings_label.place(x=230, y=5)

frets_label = tk.Label(root, text="Frets", font=("Helvetica", 12), justify="left")
frets_label.place(x=230, y=35)

strings_entry = tk.Entry(root, font=("Halvetica", 12), justify="center", highlightthickness=1, textvar=trace_strings)
strings_entry.place(x=295, y=5, width=35, height=25)

frets_entry = tk.Entry(root, font=("Halvetica", 12), justify="center", highlightthickness=1, textvar=trace_frets)
frets_entry.place(x=295, y=35, width=35, height=25)

strings_entry.insert(0, str(default_strings))
frets_entry.insert(0, str(default_frets))

root.mainloop()

