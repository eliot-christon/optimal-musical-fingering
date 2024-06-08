__author__ = "Eliot Christon"
__email__  = "eliot.christon@gmail.com"
__github__ = "eliot-christon"

def convert_to_roman(num:int) -> str:
    """Convert a number to a roman numeral"""
    if num < 1 or num > 3999:
        raise ValueError("The number {} is not in the range of a roman numeral (1-3999)".format(num))
    roman_numerals = [
        (1000, "M"), (900, "CM"), (500, "D"), (400, "CD"),
        (100, "C"), (90, "XC"), (50, "L"), (40, "XL"),
        (10, "X"), (9, "IX"), (5, "V"), (4, "IV"),
        (1, "I")
    ]
    roman = ""
    for value, letter in roman_numerals:
        while num >= value:
            roman += letter
            num -= value
    return roman