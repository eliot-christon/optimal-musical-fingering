__author__ = "Eliot Christon"
__email__  = "eliot.christon@gmail.com"
__github__ = "eliot-christon"

from typing import List
import numpy as np
import mido

class Roll:
    """Class reprensenting a midi roll for one track.
    A midi roll is a matrix where the rows are the notes and the columns are the time steps."""

    def __init__(self):
        """Constructor"""
        self.notes = np.array([])

    @classmethod
    def from_notes(cls, channel_events: List[mido.messages.Message]):
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

        roll.notes = np.zeros((note_max - note_min + 1, time_total))

        time = 0
        for event in channel_events:
            if event.type == "note_on":
                roll.notes[event.note - note_min, time:time + event.time] += 0
            elif event.type == "note_off":
                roll.notes[event.note - note_min, time:time + event.time] -= 1
            time += event.time
            
        return roll

    
    def __str__(self) -> str:
        return "Midi Roll: {} notes".format(len(self.notes))

    def __repr__(self) -> str:
        return "Midi Roll: {} notes".format(len(self.notes))


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
        
        return Roll.from_notes(notes)

    def roll_2(channel_number=4):
        from MyMidiObject import MyMidiObject
        midi_file = MyMidiObject('src/AUD_NK0155.mid')
        return Roll.from_notes(midi_file.channels_events[channel_number])

    roll = roll_2(4)


    import matplotlib.pyplot as plt

    plt.matshow(roll.notes, aspect='auto', cmap='Grays')
    # invert y axis
    plt.gca().invert_yaxis()
    plt.show()

