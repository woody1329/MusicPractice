import tkinter as tk
from tkinter import Label, Button, OptionMenu, StringVar, Entry, DoubleVar, Scale, HORIZONTAL
from PIL import Image, ImageTk, ImageChops
from music21 import stream, note, tempo
import subprocess
import threading
import time
import pygame
import fluidsynth
import os
from music21 import environment
from pathlib import Path
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
# def generate_score_png(notes, bpm, filename="score"):
#     s = stream.Stream()
#     s.append(tempo.MetronomeMark(number=bpm))
#     for n in notes:
#         s.append(note.Note(n, quarterLength=1))

#     lily_file = s.write("lilypond", fp=f"{filename}.ly")

#     subprocess.run([
#         "lilypond",
#         "-dbackend=eps",
#         "-dno-gs-load-fonts",
#         "-dinclude-eps-fonts",
#         "-dresolution=150",
#         "-fpng",
#         "-o", filename,
#         str(lily_file)
#     ], check=True)

#     return f"{filename}.png"

from music21 import stream, note, tempo
import subprocess
from pathlib import Path

# def generate_score_png(notes, bpm, filename="score"):
#     """
#     Generates a PNG of a musical score from a list of notes and a BPM.
#     Works even if `notes` is empty.
#     """
#     # Create a Score and a Part (Staff)
#     # s = stream.Score()
#     # staff = stream.Part()
    
#     # # Add tempo
#     # staff.append(tempo.MetronomeMark(number=bpm))
    
#     # # Add notes, or a placeholder if empty
#     # if notes:
#     #     for n in notes:
#     #         staff.append(note.Note(n, quarterLength=1))
#     # else:
#     #     # Placeholder note to keep LilyPond happy
#     #     staff.append(note.Rest(quarterLength=1))
    
#     # s.append(staff)

#     us = environment.UserSettings()
#     us['lilypondPath'] = r"C:\Program Files (x86)\LilyPond\bin\lilypond.exe"  # adjust if needed
#     #us['musicxmlPath'] = 'path-to-musescore-or-other-viewer'  # optional
#     #us['graphicsPath'] = 'C:\\Program Files\\LilyPond\\usr\\bin'  # so PNG export works

#     # # Write LilyPond file
#     lily_file_path = Path(f"score.ly")
#     # s.write("lilypond", fp=lily_file_path)
#     notes = ["C4","D4","E4","F4","G4","A4","B4","C5"]
#     bpm = 120

#     score = stream.Score()
#     part = stream.Part()
#     #staff = stream.Staff()
#     part.append(tempo.MetronomeMark(number=bpm))

#     for n in notes:
#         part.append(note.Note(n, quarterLength=1))

#     score.append(part)
#     ly_path = score.write('lilypond', fp='score.ly')

# # Remove offending lines
#     with open(ly_path, 'r', encoding='utf-8') as f:
#         lines = f.readlines()

#     cleaned = [line for line in lines if "RemoveEmptyStaffContext" not in line]

#     with open(ly_path, 'w', encoding='utf-8') as f:
#         f.writelines(cleaned)

#     # Now run LilyPond
#     import subprocess
#     subprocess.run([
#         "lilypond", "-fpng", "-o", "score", ly_path
#     ], check=True)

#     #score.write("lilypond.png")
#     #print(Path("score.ly").read_text(encoding="utf-8"))
#     # Call LilyPond to generate PNG
#     # try:
#     #     subprocess.run([
#     #         "lilypond",
#     #         "-dbackend=eps",
#     #         "-dno-gs-load-fonts",
#     #         "-dinclude-eps-fonts",
#     #         "-dresolution=150",
#     #         "-fpng",
#     #         "-o", filename,
#     #         str(lily_file_path)
#     #     ], check=True)
#     # except subprocess.CalledProcessError as e:
#     #     print("Error generating PNG with LilyPond:", e)
#     #     return None
    
#     return Path("lilypond.png")
import subprocess
from music21 import stream, note, tempo
from pathlib import Path
SOUNDFONT_FILE = Path.cwd() / "GeneralUser-GS.sf2"
def generate_score_png(notes, bpm, filename="score"):
    # Create the score
    s = stream.Score()
    p = stream.Part()
    p.append(tempo.MetronomeMark(number=bpm))
    for n in notes:
        p.append(note.Note(n, quarterLength=1))
    s.append(p)

    # Write LilyPond file
    ly_path = s.write("lilypond", fp=f"{filename}.ly")

    # Clean problematic lines
    ly_lines = Path(ly_path).read_text(encoding="utf-8").splitlines()
    clean_lines = [l for l in ly_lines if "RemoveEmptyStaffContext" not in l]
    Path(ly_path).write_text("\n".join(clean_lines), encoding="utf-8")

    # Run LilyPond to generate PNG
    subprocess.run([
        "lilypond",
        "-fpng",
        "-o", filename,  # output prefix
        ly_path
    ], cwd="C:/Users/Woody/Work2025/MusicPractice", check=True)
    print(os.listdir("."))
    # LilyPond names pages like filename-1.png, filename-2.png...
    png_file = Path(f"{filename}.png")
    png_file = Path(f"{filename}.png").resolve()
    print('png ile path: ', png_file)
    if not png_file.exists():
        raise FileNotFoundError(f"LilyPond did not produce {png_file}")
    return str(png_file)

# -----------------------
# AUDIO PLAYBACK
# -----------------------
# def play_program(notes, bpm):
#     # Init pygame mixer for metronome
#     pygame.mixer.init()
#     click_sound = pygame.mixer.Sound(pygame.mixer.Sound.get_buffer(
#         pygame.mixer.Sound(pygame.sndarray.make_sound(
#             pygame.sndarray.array([4096] * 200, dtype="int16")
#         ))
#     ))

#     # Init FluidSynth
#     fs = fluidsynth.Synth()
#     fs.start(driver="alsa" if not hasattr(fs, "audio_driver") else None)
#     fs.sfload(SOUNDFONT)
#     fs.program_select(0, 0, 0, 0)

#     spb = 60.0 / bpm  # seconds per beat

#     # Count-in (4 clicks)
#     for _ in range(4):
#         click_sound.play()
#         time.sleep(spb)

#     # Play notes
#     for n in notes:
#         midi_pitch = note.Note(n).pitch.midi
#         fs.noteon(0, midi_pitch, 100)
#         time.sleep(spb)
#         fs.noteoff(0, midi_pitch)

#     fs.delete()

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
        # Repeat count dropdown
        self.repeat_var = StringVar(value="1")
        self.repeat_dropdown = OptionMenu(master, self.repeat_var, *map(str, range(1, 11)))
        self.repeat_dropdown.pack(pady=5)
                # Pause duration entry (seconds)
        Label(master, text="Pause between repeats (s):").pack()
        self.pause_var = DoubleVar(value=1.0)
        self.pause_entry = Entry(master, textvariable=self.pause_var, width=5)
        self.pause_entry.pack(pady=5)
        # Play button
        self.play_btn = Button(master, text="Play", command=self.start_play)
        self.play_btn.pack(pady=10)
        self.tempo_slider = Scale(root, from_=40, to=240, orient=HORIZONTAL,
                     label="Tempo (BPM)")
        self.tempo_slider.set(120)  # default tempo
        self.tempo_slider.pack(pady=10)
        
        self.update_score(self.program_var.get())
        self.play_thread = None
        self.play_stop_event = threading.Event()
        
    def update_score(self, program_name="C Major Scale"):
        notes = programs[program_name]["notes"]
        bpm = programs[program_name].get("tempo", BPM_DEFAULT)
        png_file = generate_score_png(notes, bpm)
        img = Image.open(png_file)
        img = Image.open(png_file)
        bbox = ImageChops.invert(img.convert("L")).getbbox()  # find non-white content
        if bbox:
            img = img.crop(bbox)
        #img.thumbnail((600, 200)) 
        self.tk_img = ImageTk.PhotoImage(img)
        self.label.config(image=self.tk_img)
        self.label.image =self.tk_img  # critical

    # def start_play(self):
    #     # Run playback in a separate thread so GUI stays responsive
    #     threading.Thread(target=self.play_program_with_metronome, daemon=True).start()
    def start_play(self):
        # Signal any existing thread to stop
        if self.play_thread and self.play_thread.is_alive():
            self.play_stop_event.set()
            self.play_thread.join()  # wait for it to stop
            self.play_stop_event.clear()

        # Start new playback thread
        self.play_thread = threading.Thread(target=self.play_program_with_metronome, daemon=True)
        self.play_thread.start()
    def play_program(self):
        program_name = self.program_var.get()
        notes = programs[program_name]["notes"]
        tempo = programs[program_name].get("tempo", 120)
        beat_duration = 60 / tempo  # seconds per quarter note

        # Initialize FluidSynth
        fs = fluidsynth.Synth()
        fs.start(driver="portaudio")  # or another driver depending on OS
        sfid = fs.sfload(str(SOUNDFONT_FILE))
        fs.program_select(0, sfid, 0, 0)  # channel 0, bank 0, preset 0

        try:
            for n in notes:
                midi_num = note.Note(n).pitch.midi
                fs.noteon(0, midi_num, 120)  # channel 0, note number, velocity
                time.sleep(beat_duration)     # simple timing
                fs.noteoff(0, midi_num)
        finally:
            fs.delete()

    def play_program_with_metronome(self, tempo=120):
        program_name = self.program_var.get()
        notes = programs[program_name]["notes"]
        tempo = self.tempo_slider.get()#programs[program_name].get("tempo", 120)
        repeat = int(self.repeat_var.get())
        pause_between_repeats = self.pause_var.get()
        beat_duration = 60 / tempo  # seconds per quarter note
        fs = fluidsynth.Synth()
        fs.start(driver="dsound")
        sfid = fs.sfload(str(SOUNDFONT_FILE))
        
        # Instrument on channel 0
        fs.program_select(0, sfid, 0, 0)
        # Metronome click on channel 1 (any high pitch note)
        fs.program_select(1, sfid, 0, 0)

        try:
            
            for i in range(4):
            # click note (C6, velocity 100)
                fs.noteon(1, 84, 100)
                time.sleep(0.05)
                fs.noteoff(1, 84)
                time.sleep(beat_duration - 0.05)
            for _ in range(repeat):
                for n in notes:
                    midi_num = note.Note(n).pitch.midi
                    fs.noteon(0, midi_num, 120)  # play note
                    
                    # Play metronome click at start of beat
                    fs.noteon(1, 84, 100)  # C6
                    time.sleep(0.05)        # very short click
                    fs.noteoff(1, 84)

                    time.sleep(beat_duration - 0.05)
                    fs.noteoff(0, midi_num)
                if self.play_stop_event.is_set():
                    return  # stop if signaled
                # pause after the full sequence
                time.sleep(pause_between_repeats)
        finally:
            fs.delete()

# -----------------------
# RUN APP
# -----------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = PracticeApp(root)
    root.mainloop()
