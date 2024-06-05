__author__ = "Eliot Christon"
__email__  = "eliot.christon@gmail.com"
__github__ = "eliot-christon"

import mido

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
        self.__divide_tracks()
    
    def __divide_tracks(self):
        """Divide the tracks in 3 categories: meta data, notes and changes"""
        
        self.tracks_meta_data = [[] for _ in range(len(self.tracks))]
        self.tracks_notes     = [[] for _ in range(len(self.tracks))]
        self.tracks_changes   = [[] for _ in range(len(self.tracks))]
        self.tracks_channels  = [dict() for _ in range(len(self.tracks))]

        for i, track in enumerate(self.tracks):
            for msg in track:
                if msg.type in self.types["notes"]:
                    self.tracks_notes[i].append(msg)
                elif msg.type in self.types["changes"]:
                    self.tracks_changes[i].append(msg)
                else:
                    self.tracks_meta_data[i].append(msg)

                if "channel" in msg.dict() and msg.channel < self.max_channels:
                    if msg.channel not in self.tracks_channels[i]:
                        self.tracks_channels[i][msg.channel] = []
                    self.tracks_channels[i][msg.channel].append(msg)

    def __str__(self) -> str:
        return super().__str__()
    
    def __repr__(self) -> str:
        return super().__repr__()

if __name__ == "__main__":
    # Load the midi file
    midi_file = MidiObject('src/AUD_NK0155.mid')
    print("Midi file loaded")
    for i, track in enumerate(midi_file.tracks):
        print('\nTrack {}: {}'.format(i, track.name))
        print("  notes     :", len(midi_file.tracks_notes[i]))
        print("  changes   :", len(midi_file.tracks_changes[i]))
        print("  meta data :", len(midi_file.tracks_meta_data[i]))
        print("  channels  :", ', '.join([str(k) for k in midi_file.tracks_channels[i].keys()]))

    print(type(midi_file.tracks_notes[-2][0]))
    print(midi_file.tracks_notes[-2][0])