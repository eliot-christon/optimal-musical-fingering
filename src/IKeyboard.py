__author__ = "Eliot Christon"
__email__  = "eliot.christon@gmail.com"
__github__ = "eliot-christon"

from typing import Tuple, Dict

from .Instrument import Instrument
from .Position import Position

class IKeyboard(Instrument):
    """Class representing a keyboard instrument"""

    def __init__(self, 
                 name:str, 
                 description:str, 
                 range:Tuple[str, str], # (min, max), 0 is the lowest note (C0), 127 is the highest note (G10)
                 fingers:Dict[int, str] = {0: "left pinky", 1: "left ring", 2: "left middle", 3: "left index", 4: "left thumb", 5: "right thumb", 6: "right index", 7: "right middle", 8: "right ring", 9: "right pinky"}):
        super().__init__(name, "keyboard", description, range, fingers)

        self.overlapping_penalty_factor = 200

        self.ok_distances_matrix = [
           #   0   1   2   3   4   5   6   7   8   9
            [  0,  2,  4,  6,  9,200,200,200,200,200], # 0
            [ -1,  0,  2,  4,  7,200,200,200,200,200], # 1
            [ -1, -1,  0,  2,  5,200,200,200,200,200], # 2
            [ -1, -1, -1,  0,  3,200,200,200,200,200], # 3
            [ -1, -1, -1, -1,  0,200,200,200,200,200], # 4
            [100,100,100,100,100,  0,  3,  5,  7,  9], # 5
            [100,100,100,100,100, -1,  0,  2,  4,  6], # 6
            [100,100,100,100,100, -1, -1,  0,  2,  4], # 7
            [100,100,100,100,100, -1, -1, -1,  0,  2], # 8
            [100,100,100,100,100, -1, -1, -1, -1,  0]  # 9
        ]

    def __str__(self) -> str:
        return super().__str__()

    def __repr__(self) -> str:
        return super().__repr__()

    def __eq__(self, other) -> bool:
        return super().__eq__(other)
    
    def same_hand(self, finger_i:int, finger_j:int) -> bool:
        """Checks if two fingers are on the same hand"""
        return (finger_i < 5 and finger_j < 5) or (finger_i >= 5 and finger_j >= 5)
    
    def position_cost(self, position:Position) -> float:
        """Computes the cost of a position.
        In a keyboard instrument, the cost is for each hand
            . 0 when two fingers are below the ok distance (non overlapping <=> non negative distance)
            . the summed distance between the two fingers otherwise

        Args:
            position (Position): the position to evaluate
        """
        
        position.sort_by_finger()

        cost = 0

        for i in range(len(position)-1):
            for j in range(i+1, len(position)):
                finger_i = position.fingers[i]
                finger_j = position.fingers[j]
                distance = position.notes[j] - position.notes[i]
                ok_distance = self.ok_distances_matrix[finger_i][finger_j]

                if self.same_hand(finger_i, finger_j):
                    if distance < 0:
                        cost += self.overlapping_penalty_factor
                if distance > ok_distance:
                    cost += abs(distance) - ok_distance
        
        return cost + len(position)
    
    def hand_placements(self, position:Position) -> Tuple[float, float]:
        """Computes the placement of the two hands within one position."""
        left_hand = []
        right_hand = []

        for i in range(len(position)):
            if position.fingers[i] < 5:
                left_hand.append(position.notes[i])
            else:
                right_hand.append(position.notes[i])
        
        if len(left_hand) == 0:
            left_hand_placement = -1
        else:
            left_hand_placement = sum(left_hand) / len(left_hand)
        
        if len(right_hand) == 0:
            right_hand_placement = -1
        else:
            right_hand_placement = sum(right_hand) / len(right_hand)

        return left_hand_placement, right_hand_placement
    
    def transition_cost(self, position_1:Position, position_2:Position) -> float:
        """Computes the cost of a transition between two positions.
        The transition cost is the distance between the hands positions"""
        pos_1_full = position_1.get_full_position(len(self.fingers))
        pos_2_full = position_2.get_full_position(len(self.fingers))

        cost = 0

        for i in range(len(pos_1_full)):
            if pos_1_full.notes[i] != -1 and pos_2_full.notes[i] != -1:
                cost += abs(pos_2_full.notes[i] - pos_1_full.notes[i])
        
        hand_pos_1 = self.hand_placements(position_1)
        hand_pos_2 = self.hand_placements(position_2)

        if hand_pos_1[0] != -1 and hand_pos_2[0] != -1:
            cost += abs(hand_pos_2[0] - hand_pos_1[0])
        if hand_pos_1[1] != -1 and hand_pos_2[1] != -1:
            cost += abs(hand_pos_2[1] - hand_pos_1[1])

        return cost
                



if __name__ == "__main__":
    piano = IKeyboard("piano", "A piano", ("A0", "B8"))

    pos1 = Position([60, 64, 67], [5, 6, 7])
    print(pos1)
    print(piano.position_cost(pos1))

    pos2 = Position([60, 64, 67], [4, 5, 9])
    print(pos2)
    print(piano.position_cost(pos2))

    pos3 = Position([60, 64, 67], [0, 1, 3])
    print(pos3)
    print(piano.position_cost(pos3))

    pos4 = Position([64, 67, 70], [1, 3, 4])
    print(pos4)
    print(piano.position_cost(pos4))    

    print(piano.transition_cost(pos1, pos2))
    print(piano.transition_cost(pos3, pos4))