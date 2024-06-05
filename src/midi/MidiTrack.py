__author__ = "Eliot Christon"
__email__  = "eliot.christon@gmail.com"
__github__ = "eliot-christon"

import mido
import matplotlib.pyplot as plt

from .MidiRoll import MidiRoll

# inherit the origin mido class
class MidiTrack(mido.MidiTrack):
    """Custom class to handle midi tracks."""

    def __init__(self, track:mido.MidiTrack):
        mido.MidiTrack.__init__(self, track)
        self.notes = []
        self.changes = []
        self.meta_data = []
        self.channels = dict()

        self.__divide_events()
        self.rolls = {num : MidiRoll.from_channel_events(channel) for num, channel in self.channels.items()}

    def __divide_events(self):
        """Divide the events in 3 categories: meta data, notes and changes"""

        for msg in self:
            if msg.type in ["note_on", "note_off"]:
                self.notes.append(msg)
            elif msg.type in ["program_change", "control_change"]:
                self.changes.append(msg)
            else:
                self.meta_data.append(msg)

            if "channel" in msg.dict() and msg.type != "channel_prefix":
                if msg.channel not in self.channels:
                    self.channels[msg.channel] = []
                self.channels[msg.channel].append(msg)
    
    def __str__(self) -> str:
        return super().__str__()
    
    def __repr__(self) -> str:
        return super().__repr__()
    
    def __len__(self) -> int:
        return len(self.notes) + len(self.changes) + len(self.meta_data)
    
    def display_roll(self):
        """Display the roll of the track"""
        for i, roll in self.rolls.items():
            roll.display(title="Track {} - Channel {}".format(self.name, i))
    
if __name__ == "__main__":
    # Load the midi file
    midi_file = mido.MidiFile('AUD_NK0155.mid')
    track_num = 6
    track = MidiTrack(midi_file.tracks[track_num])
    
    track.display_roll()