__author__ = "Eliot Christon"
__email__  = "eliot.christon@gmail.com"
__github__ = "eliot-christon"

from typing import List

from .utils.note2num import note2num


class Position:
    """Class representing a position on an instrument"""

    def __init__(self, notes:List[int], fingers:List[int], id:int=None):
        self.notes = notes
        self.fingers = fingers
        self.id = id

    @classmethod
    def from_str_notes(cls, notes:List[str], fingers:List[int]):
        """Alternative constructor"""
        return cls([note2num(note) for note in notes], fingers)
    
    def __str__(self) -> str:
        return f"Notes: {self.notes}, Fingers: {self.fingers}, ID: {self.id}"
    
    def __repr__(self) -> str:
        return f"Position({self.notes}, {self.fingers}, {self.id})"

    def __len__(self) -> int:
        return len(self.notes)

    def sort_by_finger(self):
        """Sorts the notes and fingers by finger"""
        self.notes, self.fingers = map(list, zip(*sorted(zip(self.notes, self.fingers), key=lambda x: x[1])))
    
    def get_full_position(self, num_fingers:int=10) ->  "Position":
        """Returns the full position (all fingers)
        quiet notes are represented by -1
        """
        new_notes = []
        new_fingers = [i for i in range(num_fingers)]
        for i in range(num_fingers):
            if i in self.fingers:
                new_notes.append(self.notes[self.fingers.index(i)])
            else:
                new_notes.append(-1)
        return Position(new_notes, new_fingers)
        


if __name__ == "__main__":
    pos = Position([60, 62, 64, 65, 67, 69, 71, 72], [0, 1, 2, 3, 4, 6, 5, 7])
    print(pos)
    pos.sort_by_finger()
    print(pos)