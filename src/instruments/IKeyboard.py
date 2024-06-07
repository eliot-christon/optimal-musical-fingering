__author__ = "Eliot Christon"
__email__  = "eliot.christon@gmail.com"
__github__ = "eliot-christon"

from typing import Tuple, Dict

from .Instrument import Instrument
from ..Position import Position

class IKeyboard(Instrument):
    """Class representing a keyboard instrument"""

    def __init__(self, 
                 name:str = "keyboard", 
                 description:str = "A keyboard instrument", 
                 range:Tuple[str, str] = ("A0", "B8"), # (min, max), 0 is the lowest note (C0), 127 is the highest note (G10)
                 hands_separation:int = 5,
                 fingers:Dict[int, str] = {0: "left pinky", 1: "left ring", 2: "left middle", 3: "left index", 4: "left thumb", 5: "right thumb", 6: "right index", 7: "right middle", 8: "right ring", 9: "right pinky"}):
        super().__init__(name, "keyboard", description, range, fingers)

        self.hands_separation = hands_separation

        self.overlapping_penalty_factor = 200
        self.same_finger_penalty_factor = 500
        self.two_hands_penalty_factor   = 90
        self.crossing_hands_penalty_factor = 120

        self.ok_distances_matrix = [
           #   0   1   2   3   4   5   6   7   8   9
            [  0,  2,  4,  6, 10,200,200,200,200,200], # 0
            [ -1,  0,  2,  4,  8,200,200,200,200,200], # 1
            [ -1, -1,  0,  2,  6,200,200,200,200,200], # 2
            [ -1, -1, -1,  0,  4,200,200,200,200,200], # 3
            [ -1, -1, -1, -1,  0,200,200,200,200,200], # 4
            [100,100,100,100,100,  0,  4,  6,  8, 10], # 5
            [100,100,100,100,100, -1,  0,  2,  4,  6], # 6
            [100,100,100,100,100, -1, -1,  0,  2,  4], # 7
            [100,100,100,100,100, -1, -1, -1,  0,  2], # 8
            [100,100,100,100,100, -1, -1, -1, -1,  0]  # 9
        ]

        self.hand_amplitude = self.ok_distances_matrix[0][self.hands_separation - 1]

    def __str__(self) -> str:
        return super().__str__()

    def __repr__(self) -> str:
        return super().__repr__()

    def __eq__(self, other) -> bool:
        return super().__eq__(other)
    
    def same_hand(self, finger_i:int, finger_j:int) -> bool:
        """Checks if two fingers are on the same hand"""
        return (finger_i < self.hands_separation and finger_j < self.hands_separation) or (finger_i >= self.hands_separation and finger_j >= self.hands_separation)
    
    def position_cost(self, in_position:Position, display:bool=False) -> float:
        """Computes the cost of a position.
        In a keyboard instrument, the cost is for each hand
            . 0 when two fingers are below the ok distance (non overlapping <=> non negative distance)
            . the summed distance between the two fingers otherwise

        Args:
            position (Position): the position to evaluate
        """
        if display: print()
        
        position = in_position.sort_by_finger()

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
                        if display: print("Overlapping fingers: {} and {}".format(finger_i, finger_j))
                if distance > ok_distance:
                    add = abs(distance - ok_distance)**2.5 + 1
                    cost += add
                    if display: print(f"Fingers {finger_i} and {finger_j} too far: distance = {distance}, ok distance = {ok_distance}, cost = {add}")
        
        # if two times same finger in position
        for i in range(len(position)-1):
            if position.fingers[i] == position.fingers[i+1]:
                cost += self.same_finger_penalty_factor
                if display: print("Same finger used twice: {}".format(position.fingers[i]))
        
        # if two hands used and less than 6 notes and delta between max and min note is less than hand amplitude
        if len(position) <= self.hands_separation and (max(position.notes) - min(position.notes)) < self.hand_amplitude:
            if min(position.fingers) < self.hands_separation and max(position.fingers) >= self.hands_separation:
                cost += self.two_hands_penalty_factor
                if display: print(f"Two hands penalty, min note: {min(position.notes)}, max note: {max(position.notes)}, hand amplitude: {self.hand_amplitude}")
        
        # if crossing hands
        hand_placement = self.hand_placements(position)
        if hand_placement[0] != -1 and hand_placement[1] != -1 and hand_placement[0] > hand_placement[1]:
            cost += self.crossing_hands_penalty_factor
            if display: print("Crossing hands")
        
        return cost
    
    def hand_placements(self, position:Position) -> Tuple[float, float]:
        """Computes the placement of the two hands within one position."""
        left_hand = []
        right_hand = []

        for i in range(len(position)):
            if position.fingers[i] < self.hands_separation:
                left_hand.append(position.notes[i] - self.ok_distances_matrix[0][position.fingers[i]])
            else:
                right_hand.append(position.notes[i] - self.ok_distances_matrix[self.hands_separation][position.fingers[i]])
        
        if len(left_hand) == 0:
            left_hand_placement = -1
        else:
            left_hand_placement = sum(left_hand) / len(left_hand)
        
        if len(right_hand) == 0:
            right_hand_placement = -1
        else:
            right_hand_placement = sum(right_hand) / len(right_hand)

        return left_hand_placement, right_hand_placement
    
    def transition_cost(self, position_1:Position, position_2:Position, display:bool=False) -> float:
        """Computes the cost of a transition between two positions.
        The transition cost is the distance between the hands positions"""
        if display: print()
        pos_1_full = position_1.get_full_position(len(self.fingers))
        pos_2_full = position_2.get_full_position(len(self.fingers))

        cost = 0

        for i in range(len(pos_1_full)):
            if pos_1_full.notes[i] != -1 and pos_2_full.notes[i] != -1:
                add = abs(pos_2_full.notes[i] - pos_1_full.notes[i])
                cost += add
                if display and add > 0: print("Finger {}: {} -> {}, cost: {}".format(i, pos_1_full.notes[i], pos_2_full.notes[i], add))
        
        hand_pos_1 = self.hand_placements(position_1)
        hand_pos_2 = self.hand_placements(position_2)

        if hand_pos_1[0] != -1 and hand_pos_2[0] != -1:
            add = abs(hand_pos_2[0] - hand_pos_1[0]) * 2
            cost += add
            if display and add > 0: print("Left hand: {} -> {}, cost: {}".format(hand_pos_1[0], hand_pos_2[0], add))

        if hand_pos_1[1] != -1 and hand_pos_2[1] != -1:
            add = abs(hand_pos_2[1] - hand_pos_1[1]) * 2
            cost +=add
            if display and add > 0: print("Right hand: {} -> {}, cost: {}".format(hand_pos_1[1], hand_pos_2[1], add))
        
        # if different hands used for near notes (near notes are notes with a distance less than self.hand_amplitude)
        #  first check if different hands used, only right to only left or only left to only right
        if (max(position_1.fingers) < self.hands_separation and min(position_2.fingers) >= self.hands_separation) or (max(position_2.fingers) < self.hands_separation and min(position_1.fingers) >= self.hands_separation):
            if abs(max(position_1.notes) - min(position_2.notes)) < self.hand_amplitude:
                cost += self.two_hands_penalty_factor
                if display: print("Two hands penalty")
        
        # less cost if same finger on same note again
        for i in range(len(self.fingers)):
            if pos_1_full.notes[i] == pos_2_full.notes[i] and pos_1_full.fingers[i] == pos_2_full.fingers[i] and pos_1_full.notes[i] != -1:
                cost = max(0, cost - 2)
                if display: print("Same finger on same note bonus -2")

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