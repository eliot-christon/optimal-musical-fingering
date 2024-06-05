__author__ = "Eliot Christon"
__email__  = "eliot.christon@gmail.com"
__github__ = "eliot-christon"

import mido
from MidiTrack import MidiTrack

# inherit the origin mido class
class MidiObject(mido.MidiFile):
    """Custom class to handle midi files.
    New methods to plot the midi roll and extract only the notes"""

    def __init__(self, path:str, max_channels:int=16):
        """Constructor"""
        mido.MidiFile.__init__(self, path)
        self.max_channels = max_channels
        self.types = {"notes": ["note_on", "note_off"],
                      "changes": ["program_change", "control_change"]}
        self.better_tracks = [MidiTrack(track) for track in self.tracks]
            
    def __str__(self) -> str:
        return super().__str__()
    
    def __repr__(self) -> str:
        return super().__repr__()

if __name__ == "__main__":
    # Load the midi file
    midi_file = MidiObject('src/midi/AUD_NK0155.mid')
    print("Midi file loaded")
    for i, track in enumerate(midi_file.better_tracks):
        print('\nTrack {}: {}'.format(i, track.name))
        print("  notes     :", len(track.notes))
        print("  changes   :", len(track.changes))
        print("  meta data :", len(track.meta_data))
        print("  channels  :", ', '.join([str(k) for k in track.channels.keys()]))