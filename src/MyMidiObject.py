__author__ = "Eliot Christon"
__email__  = "eliot.christon@gmail.com"
__github__ = "eliot-christon"

import mido

# inherit the origin mido class
class MyMidiObject(mido.MidiFile):
    """Custom class to handle midi files.
    New methods to plot the midi roll and extract only the notes"""

    def __init__(self, path):
        """Constructor"""
        mido.MidiFile.__init__(self, path)
        self.__divide_tracks()
    
    def __divide_tracks(self):
        """Divide the tracks in 3 categories: meta data, notes and changes"""
        
        self.meta_data_tracks = [[] for _ in range(len(self.tracks))]
        self.note_tracks      = [[] for _ in range(len(self.tracks))]
        self.change_tracks    = [[] for _ in range(len(self.tracks))]

        for i, track in enumerate(self.tracks):
            for msg in track:
                if msg.type in ["note_on", "note_off"]:
                    self.note_tracks[i].append(msg)
                elif msg.type in ["program_change", "control_change"]:
                    self.change_tracks[i].append(msg)
                else:
                    self.meta_data_tracks[i].append(msg)

    def __str__(self) -> str:
        return super().__str__()
    
    def __repr__(self) -> str:
        return super().__repr__()

if __name__ == "__main__":
    # Load the midi file
    midi_file = MyMidiObject('src/AUD_NK0155.mid')
    print("Midi file loaded")
    for i, track in enumerate(midi_file.tracks):
        print('\nTrack {}: {}'.format(i, track.name))
        print("  notes     :", len(midi_file.note_tracks[i]))
        print("  changes   :", len(midi_file.change_tracks[i]))
        print("  meta data :", len(midi_file.meta_data_tracks[i]))
