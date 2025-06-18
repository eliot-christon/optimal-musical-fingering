__author__ = "Eliot Christon"
__email__  = "eliot.christon@gmail.com"
__github__ = "eliot-christon"

def num2note(num:int) -> str:
    """Convert a number to its corresponding note. (midi note number, C0 = 0, G10 = 127)"""
    if num < 0 or num > 127:
        raise ValueError("The number {} is not in the range of a midi note number (0-127)".format(num))
    notes = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    note = notes[num % 12]
    octave = num // 12
    return note + str(octave)

assert num2note(0)   == "C0"
assert num2note(1)   == "C#0"
assert num2note(12)  == "C1"
assert num2note(127) == "G10"
assert num2note(69)  == "A5"
assert num2note(49)  == "C#4"
assert num2note(46)  == "A#3"


if __name__ == "__main__":

    print("-1:", num2note(-1))