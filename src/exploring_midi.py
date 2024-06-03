import mido
from src.roll_update import MidiFile

if __name__ == "__main__" :
    print("Starting the exploring_midi.py script")
    # Load the midi file
    midi_file = mido.MidiFile('src/AUD_NK0155.mid')
    print("Midi file loaded")
    # read the midi tracks
    for i, track in enumerate(midi_file.tracks):
        print('\nTrack {}: {}'.format(i, track.name))
        print(repr(track)[:800])
    
    # listen to one track
    track_number = 10
    track = midi_file.tracks[track_number]

    # for msg in track:
    #     print(msg)
    
    # # roll (vizualize the midi file)
    # midi = MidiFile('src/AUD_NK0155.mid')
    # roll = midi.get_roll()
    # midi.draw_roll()