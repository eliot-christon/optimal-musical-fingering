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

    def __init__(self, notes:np.ndarray = None, lowest_note:int = 0, highest_note:int = 127, first_tick:int = 0):
        self.notes = notes
        self.lowest_note = lowest_note
        self.highest_note = highest_note
        self.first_tick = first_tick

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

        fig, ax = plt.subplots(figsize=(15, 5))

        # Display the notes matrix as an image with grayscale color map
        cax = ax.matshow(self.notes, aspect='auto', cmap='Greys')

        # Set the y-axis ticks and labels
        yticks = np.arange(self.highest_note - self.lowest_note + 1)
        ytick_labels = np.arange(self.lowest_note, self.highest_note + 1)
        ax.set_yticks(yticks)
        ax.set_yticklabels(ytick_labels)
        ax.set_ylabel("Notes")

        # Set the x-axis below the image
        ax.xaxis.set_ticks_position('bottom')
        ax.set_xlabel("Time steps")

        # Invert the y-axis
        ax.invert_yaxis()

        # Set the title
        ax.set_title(title, fontsize=25)

        # Show the plot
        plt.show()
    
    def divide_in_clusters(self, ticks_threshold:int) -> "List[MidiRoll]":
        """Divide the roll in serveral clusters.
        A cluster is a group of notes that are played together, means that the last note of the cluster should be far from the first note of the next cluster.
        The distance between two notes is the time between the two notes. If the time is greater than a threshold, the notes are in different clusters."""
        clusters = []
        cluster = []
        notes_transposed = self.notes.T # so the first dimension is the time steps
        for i in range(len(notes_transposed)-ticks_threshold):
            if notes_transposed[i: i + ticks_threshold].sum() == 0:
                if len(cluster) > 0:
                    clusters.append(MidiRoll(notes=np.array(cluster).T, lowest_note=self.lowest_note, highest_note=self.highest_note, first_tick=self.first_tick + i))
                    cluster = []
            else:
                cluster.append(notes_transposed[i])
        if len(cluster) > 0:
            clusters.append(MidiRoll(notes=np.array(cluster).T, lowest_note=self.lowest_note, highest_note=self.highest_note, first_tick=self.first_tick + i))
        return clusters


def display_roll_cluster(cluster:List[MidiRoll]) -> None:
    """Display a list of roll clusters in the same figure with different colors"""
    fig, ax = plt.subplots(figsize=(15, 5))

    total_ticks = max([roll.first_tick + roll.notes.shape[1] for roll in cluster])
    lowest_note = min([roll.lowest_note for roll in cluster])
    highest_note = max([roll.highest_note for roll in cluster])

    all_notes = np.zeros((highest_note - lowest_note + 1, total_ticks), dtype="int8")
    # build the notes matrix
    values = np.arange(4, 4 + len(cluster))
    np.random.shuffle(values)
    for i, roll in enumerate(cluster):
        notes = np.where(roll.notes != 0, values[i], 0)
        all_notes[roll.lowest_note - lowest_note:roll.highest_note - lowest_note + 1, roll.first_tick:roll.first_tick + roll.notes.shape[1]] = notes
    
    # Display the notes matrix as an image with zero values in black and the other values in colors
    cax = ax.matshow(all_notes, aspect='auto', cmap='inferno')
    
    # Set the y-axis ticks and labels
    yticks = np.arange(cluster[0].highest_note - cluster[0].lowest_note + 1)
    ytick_labels = np.arange(cluster[0].lowest_note, cluster[0].highest_note + 1)
    ax.set_yticks(yticks)
    ax.set_yticklabels(ytick_labels)
    ax.set_ylabel("Notes")

    # Set the x-axis below the image
    ax.xaxis.set_ticks_position('bottom')
    ax.set_xlabel("Time steps")

    # Invert the y-axis
    ax.invert_yaxis()
  
    # Set the title
    ax.set_title("Roll clusters", fontsize=25)

    # Show the plot
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



    roll = roll_2(5)
    roll.display(title="Roll 2")

    clusters = roll.divide_in_clusters(500)
    display_roll_cluster(clusters)

