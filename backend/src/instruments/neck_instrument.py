"""
This module contains the NeckInstrument class,
which represents a neck instrument and its properties.
"""

__author__ = "Eliot Christon"
__email__ = "eliot.christon@gmail.com"
__github__ = "eliot-christon"


from ..positions.neck_position import NeckPosition
from ..utils.note2num import note2num
from ..utils.num2note import num2note
from .instrument import Instrument


class NeckInstrument(Instrument):
    """Class representing a neck instrument"""

    def __init__(
        self,
        name: str = " My neck instrument",
        description: str = "A neck instrument",
        number_of_frets: int = 12,
        open_strings: list[str] = None,  # the midi notes of the open strings
        fingers: dict[int, str] = None,  # 0 is when the string is played without a finger
    ):
        if open_strings is None:
            open_strings = ["E4", "B3", "G3", "D3", "A2", "E2"]
        if fingers is None:
            fingers = {0: "0", 1: "1", 2: "2", 3: "3", 4: "4"}
        self.open_strings = [note2num(note) for note in open_strings]
        self.number_of_frets = number_of_frets
        note_range = (
            num2note(min(self.open_strings)),
            num2note(max(self.open_strings) + number_of_frets),
        )
        super().__init__(name, "Strings", description, note_range, fingers)
        self.__basic_attributes()

    def detail(self) -> dict:
        """Returns the details of the neck instrument"""
        return {
            "strings": [num2note(note) for note in self.open_strings],
            "frets": self.number_of_frets,
            "range": self.range,
            "description": self.description,
        }

    def __basic_attributes(self):
        self.string_gap_dificulty_factor = {
            (1, 2): 2.0,
            (1, 3): 1.0,
            (1, 4): 1.0,
            (2, 3): 2.0,
            (2, 4): 1.0,
            (3, 4): 2.5,
        }

        self.invalid_position_cost_penalty = 1000
        self.hand_deplacement_penalty_factor = 10.0
        self.same_finger_same_string_same_fret_bonus = 2
        self.new_finger_cost = 2
        self.in_between_strings_cost = 15

    def get_notes(self, neck_position: NeckPosition) -> list[str]:
        """Returns the notes of a position"""
        if not self.is_valid_position(neck_position):
            return [None] * len(neck_position)
        return [
            num2note(self.open_strings[neck_position.strings[i] - 1] + neck_position.frets[i])
            for i in range(len(neck_position))
        ]

    def is_valid_position(self, in_position: NeckPosition, display: bool = False) -> bool:
        """Checks if a position is valid.
        A valid position is a position where:
            - two adjacent fingers must be within 1 or 0 fret of each other
            - max and min fret must be within the range of the left hand (here 4 frets)
            - the frets must be in increasing order
            - each finger must be on a different string
            - a string doesn't exist
            - a finger doesn't exist
            - the note is not out of the range of the instrument
        """
        neck_position = in_position.sort_by_finger()

        # Check if the frets are in increasing order
        if neck_position.frets != sorted(neck_position.frets):
            if display:
                print("   Frets are not in increasing order")
            return False

        # Check if the fingers are on different strings
        if len(set(neck_position.strings)) != len(neck_position.strings):
            if display:
                print("   Fingers are on the same string")
            return False

        # Check if the max and min fret are within the range of the left hand
        # (do not count the open strings <=> fret = 0)
        try:
            min_fret = min([fret for fret in neck_position.frets if fret > 0])
            max_fret = max([fret for fret in neck_position.frets if fret > 0])

            if max_fret is not None and min_fret is not None and max_fret - min_fret > 4:
                if display:
                    print("   Max and min fret are not within the range of the left hand")
                return False
        except ValueError:
            pass

        for i in range(len(neck_position)):
            # Check if the note is out of the range of the instrument
            if neck_position.frets[i] < 0 or neck_position.frets[i] > self.number_of_frets:
                if display:
                    print("   Fret is out of the range of the instrument")
                return False

            # Check if a string doesn't exist
            if neck_position.strings[i] not in range(1, len(self.open_strings) + 1):
                if display:
                    print("   String doesn't exist")
                return False

            # Check if a finger doesn't exist
            if neck_position.fingers[i] not in self.fingers:
                if display:
                    print("   Finger doesn't exist")
                return False

            if (
                i + 1 == len(neck_position)
                or neck_position.fingers[i] == 0
                or neck_position.fingers[i + 1] == 0
            ):
                continue

            # Check if the adjacing fingers are within 1 or 0 fret of each other
            if (
                abs(neck_position.frets[i + 1] - neck_position.frets[i]) > 1
                and abs(neck_position.fingers[i + 1] - neck_position.fingers[i]) < 1
            ):
                if display:
                    print("   Fingers are not within 1 or 0 fret of each other")
                return False
        return True

    def default_fingering(self, in_position: NeckPosition) -> NeckPosition:
        """Returns the default fingering of a position.
        - place the 0 finger if the string is open (fret = 0)
        - sort the other placements by increasing fret
        - barring
            - if two placements are on the same fret and no other lower fret placements
              on lower strings, place the same finger
        - assign fingers in increasing order
        """
        neck_position = in_position.copy()

        # Sort the other placements by increasing fret
        neck_position = neck_position.sort_by_fret()

        # Barring
        current_finger = 1
        if max(neck_position.frets) == 0:
            current_finger = 0
        else:
            current_fret = min(
                [fret for fret in neck_position.frets if fret > 0] + [self.number_of_frets * 2]
            )

        barring = False
        barring_fret = 0
        for i in range(len(neck_position)):
            # Place the 0 finger if the string is open (fret = 0)
            if neck_position.frets[i] == 0:
                neck_position.fingers[i] = 0
                continue

            # Assign fingers in increasing order
            current_finger += max(neck_position.frets[i] - current_fret - 1, 0)
            neck_position.fingers[i] = current_finger
            current_fret = neck_position.frets[i]
            # check if the next placement is on the same fret (only one barring possible)
            if (
                (i != len(neck_position) - 1)
                and (neck_position.frets[i] == neck_position.frets[i + 1])
                and (barring_fret == neck_position.frets[i] or barring_fret == 0)
            ):
                # check if no other lower fret placements on lower strings
                barring = True
                for j in range(i):
                    if (
                        neck_position.frets[j] < neck_position.frets[i]
                        and neck_position.strings[j] < neck_position.strings[i]
                    ):
                        barring = False
                        break
            else:
                barring = False

            if not barring:
                current_finger += 1
            else:
                barring_fret = neck_position.frets[i]

        return neck_position

    def position_cost(
        self, position_1: NeckPosition, check_valid: bool = True, display: bool = False
    ) -> float:
        """Computes the cost of a position.
        Cost is
            if the position is not valid: self.invalid_position_cost_penalty
            the sum of the distances between the fingers strings minus 1,
                multiplied by a dificulty factor
            the hand placement (the lower the better)
            the number of in between strings not played if > 1

        Args:
            position (NeckPosition): the position to evaluate
            check_valid (bool): if True, check if the position is valid
            display (bool): if True, display the cost computation
        """
        # if needed check if the position is valid, else return the invalid position cost penalty
        if display:
            print()

        if check_valid and not self.is_valid_position(position_1, display):
            return self.invalid_position_cost_penalty

        cost = 0.0

        # Compute the cost of the in between strings not played
        # = number of gaps * self.in_between_strings_cost
        gaps = 0
        if len(position_1) > 3:
            for i in range(1, len(position_1) - 1):
                if position_1.strings[i] != position_1.strings[i + 1] + 1:
                    gaps += 1
        cost += gaps * self.in_between_strings_cost
        if gaps > 0 and display:
            print(f"Gaps: {gaps}, penalty: {gaps * self.in_between_strings_cost}")

        # Compute the cost of the string gap
        for i in range(len(position_1) - 1):
            for j in range(i + 1, len(position_1)):
                finger_i = position_1.fingers[i]
                finger_j = position_1.fingers[j]
                if finger_i == 0 or finger_j == 0:
                    continue
                if finger_i != finger_j:
                    gap = abs(position_1.strings[j] - position_1.strings[i])
                    finger_pair = tuple(sorted([finger_i, finger_j]))
                    if finger_pair in self.string_gap_dificulty_factor:
                        cost += self.string_gap_dificulty_factor[finger_pair] * gap
                        if display:
                            print(
                                f"Fingers {finger_i} and {finger_j}, gap = {gap}, \
cost = {self.string_gap_dificulty_factor[finger_pair] * gap}"
                            )
                    else:
                        if display:
                            print(f"No dificulty factor for fingers {finger_i} and {finger_j}")
                        return self.invalid_position_cost_penalty
        cost += self.hand_placements(position_1)
        if display:
            print(f"Hand placement cost: {self.hand_placements(position_1)}")

        return cost

    def possible_places_one_note(self, note: int) -> list[tuple[int, int]]:
        """Returns the possible places of a note on the neck.
        Returns a list of tuples (string, fret)."""
        places = []
        for string, open_note in enumerate(self.open_strings):
            for fret in range(self.number_of_frets):
                if open_note + fret == note:
                    places.append((string + 1, fret))
        return places

    def possible_positions(self, note_list: list[int]) -> list[NeckPosition]:
        """Returns the possible positions of a list of notes on the neck."""
        if len(note_list) == 0:
            return []
        if len(note_list) == 1:
            no_finger_pos = []
            for string, fret in self.possible_places_one_note(note_list[0]):
                no_finger_pos.append(NeckPosition.from_strings_frets([0], [string], [fret]))
        else:
            # Recursive function to compute the possible positions, finger is 0
            def compute_positions(
                note_list: list[int], position_list: list[NeckPosition], index: int
            ) -> list[NeckPosition]:
                """Recursive function to compute the possible positions.
                Using the NeckPosition().add_note"""
                if index == len(note_list):
                    return position_list
                new_positions = []
                for current_position in position_list:
                    for place in self.possible_places_one_note(note_list[index]):
                        new_position = current_position.copy()
                        new_position.add_note(place[0], place[1], 0)
                        new_positions.append(new_position)
                return compute_positions(note_list, new_positions, index + 1)

            no_finger_pos = compute_positions(note_list, [NeckPosition([], [])], 0)
        default_finger_pos = [self.default_fingering(position) for position in no_finger_pos]
        # now shift all the positions while finger 4 isn't used
        res = []
        for current_position in default_finger_pos:
            while (max(current_position.fingers) < 4 and max(current_position.fingers) > 0) and (
                not current_position.is_barre()
            ):
                res.append(current_position.copy())
                current_position.shift(1)
            res.append(current_position)
        return res

    def hand_placements(self, neck_position: NeckPosition) -> float:
        """Computes the placement of the left hand within one position."""
        left_hand = []
        for finger, fret in zip(neck_position.fingers, neck_position.frets, strict=False):
            if finger > 0:
                left_hand.append(fret - finger)
        if len(left_hand) == 0:
            return -1
        return abs(sum(left_hand) / len(left_hand))

    def transition_cost(
        self, position_1: NeckPosition, position_2: NeckPosition, display: bool = False
    ) -> float:
        """Computes the cost of a transition between two positions.
        The transition cost is:
            the sum of the distances between the fingers strings
            the cost of the new fingers
            the difference between the hands placements by self.hand_deplacement_penalty_factor
            bonus for same finger on same string and same fret
        """
        if display:
            print()

        cost = 0.0

        for j in range(len(position_2)):
            for i in range(len(position_1)):
                if position_1.fingers[i] == position_2.fingers[j]:
                    add = abs(position_2.strings[j] - position_1.strings[i])
                    cost += add
                    if display and add > 0:
                        print(
                            f"Finger {position_1.fingers[i]}: {position_1.strings[i]} -> \
{position_2.strings[j]}, cost: {add}"
                        )

                if (
                    position_1.strings[i] == position_2.strings[j]
                    and position_1.frets[i] == position_2.frets[j]
                    and position_1.fingers[i] == position_2.fingers[j]
                ):
                    cost -= self.same_finger_same_string_same_fret_bonus
                    if display:
                        print("Same finger on same string and same fret")

            if position_2.fingers[j] not in position_1.fingers and position_2.fingers[j] != 0:
                add = self.new_finger_cost
                cost += add
                if display:
                    print(f"New finger {position_2.fingers[j]}, cost: {add}")

        hand_pos_1 = self.hand_placements(position_1)
        hand_pos_2 = self.hand_placements(position_2)

        if hand_pos_1 == -1 or hand_pos_2 == -1:
            add = 0
        else:
            add = abs(hand_pos_2 - hand_pos_1) * self.hand_deplacement_penalty_factor
        cost += add

        if display and add > 0:
            print(f"Left hand: {hand_pos_1} -> {hand_pos_2}, cost: {add}")

        return cost


class Guitar(NeckInstrument):
    """Class representing a guitar instrument"""

    def __init__(self):
        super().__init__(
            "guitar",
            "Basic guitar",
            number_of_frets=12,
            open_strings=["E4", "B3", "G3", "D3", "A2", "E2"],
        )


class Ukulele(NeckInstrument):
    """Class representing a ukulele instrument"""

    def __init__(self):
        super().__init__(
            "ukulele", "Basic ukulele", number_of_frets=12, open_strings=["A4", "E4", "C4", "G4"]
        )


class Banjo(NeckInstrument):
    """Class representing a banjo instrument"""

    def __init__(self):
        super().__init__(
            "banjo", "Basic banjo", number_of_frets=12, open_strings=["D4", "B3", "G3", "D3", "G4"]
        )


class Bass(NeckInstrument):
    """Class representing a bass instrument"""

    def __init__(self):
        super().__init__(
            "bass", "Basic bass", number_of_frets=12, open_strings=["G2", "D2", "A1", "E1"]
        )


class Mandolin(NeckInstrument):
    """Class representing a mandolin instrument"""

    def __init__(self):
        super().__init__(
            "mandolin",
            "Basic mandolin",
            number_of_frets=18,
            open_strings=["E5", "E5", "A4", "A4", "D4", "D4", "G4", "G4"],
        )


class Guitarlele(NeckInstrument):
    """Class representing a guitarlele instrument"""

    def __init__(self):
        super().__init__(
            "guitarlele",
            "Basic guitarlele",
            number_of_frets=12,
            open_strings=["A4", "E4", "C4", "G3", "D3", "A2"],
        )


if __name__ == "__main__":
    guitar = Guitar()

    pos1 = NeckPosition([300, 103, 201], [0, 3, 1])
    Fmaj7 = NeckPosition.from_strings_frets(
        fingers=[1, 3, 2, 4], strings=[6, 4, 3, 2], frets=[1, 3, 2, 3]
    )
    Amaj7 = NeckPosition.from_strings_frets(
        fingers=[0, 1, 2, 3, 0], strings=[5, 4, 3, 2, 1], frets=[0, 2, 2, 2, 0]
    )
    Dmin7 = NeckPosition.from_strings_frets(
        fingers=[0, 2, 3, 1], strings=[4, 3, 2, 1], frets=[0, 2, 3, 1]
    )

    for position in [Fmaj7, Amaj7, Dmin7]:
        print(position)
        print("Notes:", guitar.get_notes(position))
        print(guitar.position_cost(position))

    NOTE_NUM = note2num("C4")
    print("Possible places for C4:", guitar.possible_places_one_note(NOTE_NUM))

    notes = [note2num(note) for note in ["E4"]]
    # ['A2', 'F#3', 'C4', 'E4'], ['A2', 'G3', 'D4', 'E4']
    print("Possible positions for notes:", notes)
    positions = guitar.possible_positions(notes)
    for position in positions:
        if guitar.is_valid_position(position):
            position = position.sort_by_string()
            print("Valid position:", position)
            print("Notes:", guitar.get_notes(position))
            print(guitar.position_cost(position, display=False))
