__author__ = "Eliot Christon"
__email__  = "eliot.christon@gmail.com"
__github__ = "eliot-christon"

from typing import List
import numpy as np
import matplotlib.pyplot as plt
import mido

class MidiRoll:
    """Class reprensenting a midi roll for one channel.
    A midi roll is a matrix where the rows are the notes and the columns are the time steps."""

    def __init__(self):
        self.notes = np.array([], dtype="bool")
        self.lowest_note = 0
        self.highest_note = 127

    @classmethod
    def from_channel_events(cls, channel_events: List[mido.messages.Message]):
        """Create a midi roll from a list of notes"""
        roll = cls()
        note_min = 1e6
        note_max = 0
        time_total = 0
        for event in channel_events:
            if "note" in event.dict():
                note_min = min(note_min, event.note)
                note_max = max(note_max, event.note)
            if "time" in event.dict():
                time_total += event.time

        roll.notes = np.zeros((note_max - note_min + 1, time_total), dtype="int8")
        roll.lowest_note = note_min
        roll.highest_note = note_max

        time = 0
        old_time_step = 0
        for event in channel_events:

            if event.time == 0:
                time -= old_time_step
                new_time_step = old_time_step
            else:
                new_time_step = event.time

            # if event.type == "note_on":
            #     roll.notes[event.note - note_min, time:time + new_time_step] += 0
            if event.type == "note_off":
                roll.notes[event.note - note_min, time:time + new_time_step] = -1

            old_time_step = new_time_step
            time += new_time_step
            
        return roll
    
    def __str__(self) -> str:
        return "Midi Roll: {} notes".format(len(self.notes))

    def __repr__(self) -> str:
        return "Midi Roll: {} notes".format(len(self.notes))

    def display(self, title:str=""):
        """Display the midi roll"""
        plt.matshow(self.notes, aspect='auto', cmap='Grays')
        # y labels
        plt.yticks(np.arange(self.highest_note - self.lowest_note + 1), np.arange(self.lowest_note, self.highest_note + 1))
        # invert y axis
        plt.gca().invert_yaxis()
        plt.title(title, fontsize=15)
        plt.title(title, fontsize=15)
        plt.show()


if __name__ == "__main__":
    # create a midi roll from a list of notes

    def roll_1():
        notes = [mido.Message('note_on', note=60, time=0),
                mido.Message('note_off', note=60, time=100),
                mido.Message('note_on', note=62, time=100),
                mido.Message('note_off', note=62, time=100),
                mido.Message('note_on', note=64, time=200),
                mido.Message('note_off', note=64, time=100),
                mido.Message('note_on', note=65, time=300),
                mido.Message('note_off', note=65, time=100)]
        
        return MidiRoll.from_channel_events(notes)

    def roll_2(track_number=5):
        from .MidiObject import MidiObject
        midi_file = MidiObject('src/midi/AUD_NK0155.mid')
        track = midi_file.better_tracks[track_number]
        print("Track {}: {}".format(track_number, track.name))
        return track.get_first_roll()

    roll = roll_2(6)
    roll.display(title="Roll 2")

