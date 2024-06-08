__author__ = "Eliot Christon"
__email__  = "eliot.christon@gmail.com"
__github__ = "eliot-christon"

from typing import Tuple, Dict, List

from .Instrument import Instrument
from ..Position import NPosition
from ..utils.note2num import note2num
from ..utils.num2note import num2note

class INeck(Instrument):
    """Class representing a keyboard instrument"""

    def __init__(self, 
                 name:str = " My neck instrument", 
                 description:str = "A neck instrument", 
                 number_of_frets:int = 12,
                 open_strings:List[str] = ["E4", "B3", "G3", "D3", "A2", "E2"], # the midi notes of the open strings
                 fingers:Dict[int, str] = {0: "0", 1: "1", 2: "2", 3: "3", 4: "4"}, # 0 is when the string is played without a finger
               ): 
        self.open_strings = [note2num(note) for note in open_strings]
        self.number_of_frets = number_of_frets
        range = (num2note(min(self.open_strings)), num2note(max(self.open_strings) + number_of_frets))
        super().__init__(name, "Strings", description, range, fingers)
        self.__basic_attributes()
        
        
    def __basic_attributes(self):
        self.string_gap_dificulty_factor = {
            (1, 2) : 2.0,
            (1, 3) : 1.0,
            (1, 4) : 1.0,
            (2, 3) : 2.0,
            (2, 4) : 1.0,
            (3, 4) : 2.5,
        }
        
        self.invalid_position_cost_penalty = 1000
        self.hand_deplacement_penalty_factor = 3.0
        self.same_finger_same_string_same_fret_bonus = 2
        self.new_finger_cost = 2

    def __str__(self) -> str:
        return super().__str__()

    def __repr__(self) -> str:
        return super().__repr__()

    def __eq__(self, other) -> bool:
        return super().__eq__(other)
    
    def get_notes(self, position:NPosition) -> List[str]:
        """Returns the notes of a position"""
        if not self.is_valid_position(position):
            return [None] * len(position)
        return [num2note(self.open_strings[position.strings[i] - 1] + position.frets[i]) for i in range(len(position))]

    def is_valid_position(self, in_position:NPosition, display:bool=False) -> bool:
        """Checks if a position is valid.
        A valid position is a position where:
            - two adjacent fingers must be within 1 or 0 fret of each other
            - the frets must be in increasing order
            - each finger must be on a different string
            - a string doesn't exist
            - a finger doesn't exist
            - the note is not out of the range of the instrument
        """
        position = in_position.sort_by_finger()
                
        # Check if the frets are in increasing order
        if position.frets != sorted(position.frets):
            if display: print("   Frets are not in increasing order")
            return False
        
        # Check if the fingers are on different strings
        if len(set(position.strings)) != len(position.strings):
            if display: print("   Fingers are on the same string")
            return False
        
        for i in range(len(position)):
            
            # Check if the note is out of the range of the instrument
            if position.frets[i] < 0 or position.frets[i] > self.number_of_frets:
                if display: print("   Fret is out of the range of the instrument")
                return False
            
            # Check if a string doesn't exist
            if position.strings[i] not in range(1, len(self.open_strings)+1):
                if display: print("   String doesn't exist")
                return False
            
            # Check if a finger doesn't exist
            if position.fingers[i] not in self.fingers:
                if display: print("   Finger doesn't exist")
                return False
            
            if i+1 == len(position) or position.fingers[i] == 0 or position.fingers[i+1] == 0:
                continue
            
            # Check if the adjacing fingers are within 1 or 0 fret of each other
            if abs(position.placements[i+1] - position.placements[i]) > 1 and abs(position.fingers[i+1] - position.fingers[i]) < 1:
                if display: print("   Fingers are not within 1 or 0 fret of each other")
                return False
        return True
        
     
    def position_cost(self, position:NPosition, check_valid:bool=True, display:bool=False) -> float:
        """Computes the cost of a position.
        Cost is
            if the position is not valid: self.invalid_position_cost_penalty
            the sum of the distances between the fingers strings minus 1, multiplied by a dificulty factor
            the hand placement (the lower the better)
        
        Args:
            position (NPosition): the position to evaluate
            check_valid (bool): if True, check if the position is valid
            display (bool): if True, display the cost computation
        """
        # if needed check if the position is valid, else return the invalid position cost penalty
        if display: print()
        
        if check_valid and not self.is_valid_position(position, display):
            return self.invalid_position_cost_penalty
        
        cost = 0.
        
        # Compute the cost of the string gap
        for i in range(len(position)-1):
            for j in range(i+1, len(position)):
                finger_i = position.fingers[i]
                finger_j = position.fingers[j]
                if finger_i == 0 or finger_j == 0:
                    continue
                if finger_i != finger_j:
                    gap = abs(position.strings[j] - position.strings[i])
                    finger_pair = tuple(sorted([finger_i, finger_j]))
                    if finger_pair in self.string_gap_dificulty_factor:
                        cost += self.string_gap_dificulty_factor[finger_pair] * gap
                        if display: print("Fingers {} and {}, gap = {}, cost = {}".format(finger_i, finger_j, gap, self.string_gap_dificulty_factor[finger_pair] * gap))
                    else:
                        if display: print("No dificulty factor for fingers {} and {}".format(finger_i, finger_j))
                        return self.invalid_position_cost_penalty
        cost += self.hand_placements(position)
        if display: print("Hand placement cost: {}".format(self.hand_placements(position)))
        
        return cost
    
    def hand_placements(self, position:NPosition) -> float:
        """Computes the placement of the left hand within one position."""
        left_hand = []
        for finger, fret in zip(position.fingers, position.frets):
            if finger > 0:
                left_hand.append(fret - finger + 1)
        if len(left_hand) == 0:
            return 1
        return sum(left_hand) / len(left_hand)
        
    def transition_cost(self, position_1:NPosition, position_2:NPosition, display:bool=False) -> float:
        """Computes the cost of a transition between two positions.
        The transition cost is:
            the sum of the distances between the fingers strings
            the cost of the new fingers
            the difference between the hands placements by self.hand_deplacement_penalty_factor
            bonus for same finger on same string and same fret
        """
        if display: print()        
        
        cost = 0.
        
        for j in range(len(position_2)):
            for i in range(len(position_1)):
                
                if position_1.fingers[i] == position_2.fingers[j]:
                    add = abs(position_2.strings[j] - position_1.strings[i])
                    cost += add
                    if display and add > 0: print("Finger {}: {} -> {}, cost: {}".format(position_1.fingers[i], position_1.strings[i], position_2.strings[j], add))
                
                if position_1.strings[i] == position_2.strings[j] and position_1.frets[i] == position_2.frets[j] and position_1.fingers[i] == position_2.fingers[j]:
                    cost -= self.same_finger_same_string_same_fret_bonus
                    if display: print("Same finger on same string and same fret")
                
            if position_2.fingers[j] not in position_1.fingers and position_2.fingers[j] != 0:
                add = self.new_finger_cost
                cost += add
                if display: print("New finger {}, cost: {}".format(position_2.fingers[j], add))
        
        hand_pos_1 = self.hand_placements(position_1)
        hand_pos_2 = self.hand_placements(position_2)
        
        add = abs(hand_pos_2 - hand_pos_1) * self.hand_deplacement_penalty_factor
        cost += add
        
        if display and add > 0: print("Left hand: {} -> {}, cost: {}".format(hand_pos_1, hand_pos_2, add))
    
        return cost


class Guitar(INeck):
    """Class representing a guitar instrument"""
    def __init__(self):
        super().__init__("guitar", "Basic guitar", number_of_frets=12, open_strings=["E4", "B3", "G3", "D3", "A2", "E2"])


class Ukulele(INeck):
    """Class representing a ukulele instrument"""
    def __init__(self):
        super().__init__("ukulele", "Basic ukulele", number_of_frets=12, open_strings=["A4", "E4", "C4", "G4"])


if __name__ == "__main__":
    guitar = Ukulele()

    pos1 = NPosition([300, 103, 201], [0, 3, 1])
    Fmaj7 = NPosition.from_strings_frets(fingers=[1, 3, 2, 4], strings=[6, 4, 3, 2], frets=[1, 3, 2, 3])
    Amaj7 = NPosition.from_strings_frets(fingers=[0, 1, 2, 3, 0], strings=[5, 4, 3, 2, 1], frets=[0, 2, 2, 2, 0])
    Dmin7 = NPosition.from_strings_frets(fingers=[0, 2, 3, 1], strings=[4, 3, 2, 1], frets=[0, 2, 3, 1])
    
    for position in [Fmaj7, Amaj7, Dmin7]:
        print(position)
        print("Notes:", guitar.get_notes(position))
        print(guitar.position_cost(position))
