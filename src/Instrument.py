__author__ = "Eliot Christon"
__email__  = "eliot.christon@gmail.com"
__github__ = "eliot-christon"

from typing import Tuple, Dict
from utils.note2num import note2num

class Instrument:
    """Class representing an instrument"""

    def __init__(self, 
                 name:str, 
                 family:str, 
                 description:str, 
                 range:Tuple[str, str], # (min, max), 0 is the lowest note (C0), 127 is the highest note (G10)
                 fingers:Dict[int, str] = {0: "left pinky", 1: "left ring", 2: "left middle", 3: "left index", 4: "left thumb", 5: "right thumb", 6: "right index", 7: "right middle", 8: "right ring", 9: "right pinky"}):
        self.name = name
        self.family = family
        self.description = description
        self.range = (note2num(range[0]), note2num(range[1]))
        self.fingers = fingers

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return self.name

    def __eq__(self, other) -> bool:
        if not isinstance(other, Instrument):
            return False
        for attr in self.__dict__:
            if getattr(self, attr) != getattr(other, attr):
                return False
        return True




if __name__ == "__main__":

    piano = Instrument("piano", "keyboard", "A piano", ("A0", "B8"), fingers={i:str(i+1) for i in range(10)})
    guitar = Instrument("guitar", "string", "A guitar", ("E2", "E5"), fingers={0: "4", 1: "3", 2: "2", 3: "1", 5: "p", 6: "i", 7: "m", 8: "a"})
