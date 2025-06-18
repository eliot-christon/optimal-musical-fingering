__author__ = "Eliot Christon"
__email__  = "eliot.christon@gmail.com"
__github__ = "eliot-christon"

from typing import List, Tuple

from .utils.note2num import note2num
from .utils.roman_numerals import convert_to_roman


class Position:
    """Class representing a position on an instrument"""

    def __init__(self, placements:List[int], fingers:List[int], id:int=None):
        self.placements = list(placements)
        self.fingers = list(fingers)
        self.id = id

    @classmethod
    def from_str_notes(cls, notes:List[str], fingers:List[int]):
        """Alternative constructor"""
        return cls([note2num(note) for note in notes], fingers)
    
    def __str__(self) -> str:
        return f"Placement: {self.placements}, Fingers: {self.fingers}, ID: {self.id}"
    
    def __repr__(self) -> str:
        return f"Position({self.placements}, {self.fingers}, {self.id})"

    def __len__(self) -> int:
        return len(self.placements)

    def sort_by_finger(self) -> "Position":
        """Sorts the placements and fingers by finger"""
        placements, fingers = map(list, zip(*sorted(zip(self.placements, self.fingers), key=lambda x: x[1])))
        return Position(placements, fingers, self.id)
    
    def sort_by_placement(self) -> "Position":
        """Sorts the placements and fingers by placement"""
        placements, fingers = map(list, zip(*sorted(zip(self.placements, self.fingers), key=lambda x: x[0])))
        return Position(placements, fingers, self.id)
    
    def get_full_position(self, num_fingers:int=10) ->  "Position":
        """Returns the full position (all fingers)
        quiet placements are represented by -1
        """
        new_placements = []
        new_fingers = [i for i in range(num_fingers)]
        for i in range(num_fingers):
            if i in self.fingers:
                new_placements.append(self.placements[self.fingers.index(i)])
            else:
                new_placements.append(-1)
        return Position(new_placements, new_fingers)
    
    def copy(self):
        """Returns a copy of the position"""
        return Position(self.placements.copy(), self.fingers.copy(), self.id)


class NPosition(Position):
    """Class representing a position on a neck instrument. The position now gets a number of strings and frets"""
    
    def __init__(self, placements:List[int], fingers:List[int], id:int=None):
        super().__init__(list(placements), list(fingers), id)
    
    @classmethod
    def from_strings_frets(cls, fingers:List[int], strings:List[int], frets:List[int], id:int=None):
        """Alternative constructor"""
        placements = cls.convertStringsFretsToPlacements(None, strings=list(strings), frets=list(frets))
        return cls(placements, list(fingers), id)
    
    @classmethod
    def from_position(cls, position:Position):
        """Alternative constructor"""
        return cls(position.placements, position.fingers, position.id)
    
    def __str__(self) -> str:
        roman_frets = [convert_to_roman(fret) for fret in self.frets]
        return f"Strings: {self.strings}, Frets: {roman_frets}, Fingers: {self.fingers}, ID: {self.id}"
    
    def __repr__(self) -> str:
        return f"NPosition({self.placements}, {self.fingers}, {self.id})"
    
    def to_json(self) -> dict:
        """Returns the position as a json"""
        return {"strings": self.strings, "frets": self.frets, "fingers": self.fingers, "id": self.id}
        
    def sort_by_string(self, reverse=True) -> "NPosition":
        """Sorts the placements and fingers by string"""
        sorted_placements, sorted_fingers = map(list, zip(*sorted(zip(self.placements, self.fingers), key=lambda x: x[0], reverse=reverse)))
        return NPosition(sorted_placements, sorted_fingers, self.id)
    
    def sort_by_fret(self) -> "NPosition":
        """Sorts the placements and fingers by fret"""
        sorted_placements, sorted_fingers = map(list, zip(*sorted(zip(self.placements, self.fingers), key=lambda x: x[0]%100)))
        return NPosition(sorted_placements, sorted_fingers, self.id)
        
    def sort_by_finger(self) -> "NPosition":
        """Sorts the placements and fingers by finger"""
        placements, fingers = map(list, zip(*sorted(zip(self.placements, self.fingers), key=lambda x: x[1])))
        return NPosition(placements, fingers, self.id)
    
    def convertStringsFretsToPlacements(self, strings:List[int], frets:List[int]) -> List[int]:
        """Converts a list of strings and frets to a list of placements. this assumes that threr is less than 100 frets on one string."""
        return [string*100 + fret for string, fret in zip(strings, frets)]
    
    @property
    def strings(self) -> List[int]:
        """Returns the strings of the position"""
        return [note//100 for note in self.placements]
    
    @property
    def frets(self) -> List[int]:
        """Returns the frets of the position"""
        return [note%100 for note in self.placements]
    
    def add_note(self, string:int, fret:int, finger:int):
        """Adds a note to the position"""
        self.placements.append(string*100 + fret)
        self.fingers.append(finger)
    
    def get_full_position(self, num_strings:int=6) ->  "NPosition":
        """Returns the full position (all strings)
        quiet placements are represented by -1 (0 is playing the open string)
        """
        new_placements = []
        for i in range(num_strings):
            if i in self.strings:
                new_placements.append(self.placements[self.strings.index(i)])
            else:
                new_placements.append(-1)
        return NPosition(new_placements, self.fingers)
    
    def shift(self, shift:int, max_finger:int=4) -> None:
        """Shifts the position by a number of fingers.
        Only non-quiet placements are shifted if max_finger doesn't occur in the position"""
        if max_finger in self.fingers or max(self.fingers) + shift > max_finger:
            return
        # if finger > 0, shift finger
        new_fingers = []
        for i in range(len(self.placements)):
            if self.fingers[i] > 0:
                new_fingers.append(self.fingers[i] + shift)
            else:
                new_fingers.append(self.fingers[i])
        self.fingers = new_fingers

    def is_barre(self) -> bool:
        """Returns True if the position is a barre.
        is barre when same finger > 0 on multiple strings"""
        non_quiet_fingers = [finger for finger in self.fingers if finger > 0]
        return len(non_quiet_fingers) != len(set(non_quiet_fingers))


    def copy(self):
        """Returns a copy of the position"""
        return NPosition(self.placements.copy(), self.fingers.copy(), self.id)
        
    


if __name__ == "__main__":
    pos = Position([60, 62, 64, 65, 67, 69, 71, 72], [0, 1, 2, 3, 4, 6, 5, 7])
    print(pos)
    pos = pos.sort_by_finger()
    print(pos)
    
    npos = NPosition.from_strings_frets(frets=[1, 2, 0], fingers=[2, 1, 0], strings=[0, 2, 1])
    print(npos)
    npos = npos.sort_by_fret()
    print(npos)
    