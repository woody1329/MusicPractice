import tkinter as tk
from tkinter import Label, Button, OptionMenu, StringVar
from PIL import Image, ImageTk
from music21 import stream, note, tempo
import subprocess
import threading
import time
import pygame
import fluidsynth
from music21 import environment

env = environment.UserSettings()
env['lilypondPath'] = r"C:\Program Files (x86)\LilyPond\bin\lilypond.exe"

# -----------------------
# CONFIG
# -----------------------
SOUNDFONT = "./FluidR3_GM.sf2"   # <-- update this to your .sf2 file
BPM_DEFAULT = 80

programs = {
    "C Major Scale": {
        "notes": ["C4", "D4", "E4", "F4", "G4", "A4", "B4", "C5"],
        "tempo": 80
    },
    "Arpeggio": {
        "notes": ["C4", "E4", "G4", "C5"],
        "tempo": 100
    }
}

# -----------------------
# SCORE GENERATION
# -----------------------
def generate_score_png(notes, bpm, filename="score"):
    s = stream.Stream()
    s.append(tempo.MetronomeMark(number=bpm))
    for n in notes:
        s.append(note.Note(n, quarterLength=1))

    lily_file = s.write("lilypond", fp=f"{filename}.ly")

    subprocess.run([
        "lilypond",
        "-dbackend=eps",
        "-dno-gs-load-fonts",
        "-dinclude-eps-fonts",
        "-dresolution=150",
        "-fpng",
        "-o", filename,
        str(lily_file)
    ], check=True)

    return f"{filename}.png"

# -----------------------
# AUDIO PLAYBACK
# -----------------------
def play_program(notes, bpm):
    # Init pygame mixer for metronome
    pygame.mixer.init()
    click_sound = pygame.mixer.Sound(pygame.mixer.Sound.get_buffer(
        pygame.mixer.Sound(pygame.sndarray.make_sound(
            pygame.sndarray.array([4096] * 200, dtype="int16")
        ))
    ))

    # Init FluidSynth
    fs = fluidsynth.Synth()
    fs.start(driver="alsa" if not hasattr(fs, "audio_driver") else None)
    fs.sfload(SOUNDFONT)
    fs.program_select(0, 0, 0, 0)

    spb = 60.0 / bpm  # seconds per beat

    # Count-in (4 clicks)
    for _ in range(4):
        click_sound.play()
        time.sleep(spb)

    # Play notes
    for n in notes:
        midi_pitch = note.Note(n).pitch.midi
        fs.noteon(0, midi_pitch, 100)
        time.sleep(spb)
        fs.noteoff(0, midi_pitch)

    fs.delete()

# -----------------------
# GUI
# -----------------------
class PracticeApp:
    def __init__(self, master):
        self.master = master
        master.title("Practice Companion")

        # Dropdown
        self.program_var = StringVar(value=list(programs.keys())[0])
        self.dropdown = OptionMenu(master, self.program_var, *programs.keys(), command=self.update_score)
        self.dropdown.pack(pady=10)

        # Score image
        self.label = Label(master)
        self.label.pack(pady=10)

        # Play button
        self.play_btn = Button(master, text="Play", command=self.start_play)
        self.play_btn.pack(pady=10)

        self.update_score(self.program_var.get())

    def update_score(self, program_name):
        notes = programs[program_name]["notes"]
        bpm = programs[program_name].get("tempo", BPM_DEFAULT)
        png_file = generate_score_png(notes, bpm)
        img = Image.open(png_file)
        self.tk_img = ImageTk.PhotoImage(img)
        self.label.config(image=self.tk_img)

    def start_play(self):
        program_name = self.program_var.get()
        notes = programs[program_name]["notes"]
        bpm = programs[program_name].get("tempo", BPM_DEFAULT)
        threading.Thread(target=play_program, args=(notes, bpm), daemon=True).start()

# -----------------------
# RUN APP
# -----------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = PracticeApp(root)
    root.mainloop()
