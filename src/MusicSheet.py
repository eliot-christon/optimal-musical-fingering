__author__ = "Eliot Christon"
__email__  = "eliot.christon@gmail.com"
__github__ = "eliot-christon"

from typing import List

from Position import Position

class MusicSheet:
    """Class representing a music sheet (only one track)"""

    def __init__(self, title:str, positions:List[Position]):
        self.title = title
        self.positions = positions
    
    def __str__(self) -> str:
        str_pos = "\n  - ".join([str(pos) for pos in self.positions])
        return f"MusicSheet - {self.title}\n  - {str_pos}\n"

    def __repr__(self) -> str:
        return f"MusicSheet({self.title}, {self.positions})"


if __name__ == "__main__":

    pos1 = Position([60, 64, 67], [5, 6, 7], 500)
    pos2 = Position([60, 64, 67], [4, 5, 9], 800)
    pos3 = Position([60, 64, 67], [0, 1, 3], 1000)
    pos4 = Position([64, 67, 70], [1, 3, 4], 1230)
    sheet = MusicSheet(title="test", positions=[pos1, pos2, pos3, pos4])
    print(sheet)