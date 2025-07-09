"""
This module contains a function to convert numbers to Roman numerals.
Romans numerals are a numeral system originating from ancient Rome,
using combinations of letters from the Latin alphabet (I, V, X, L, C, D, M).
"""

__author__ = "Eliot Christon"
__email__ = "eliot.christon@gmail.com"
__github__ = "eliot-christon"

from .constants import MAX_ROMAN_NUMERAL, MIN_ROMAN_NUMERAL


def convert_to_roman(num: int) -> str:
    """Convert a number to a roman numeral"""
    if num == 0:
        return "-"

    if num < MIN_ROMAN_NUMERAL or num > MAX_ROMAN_NUMERAL:
        raise ValueError(f"The number {num} is not in the range of a roman numeral (1-3999)")

    roman_numerals = [
        (1000, "M"),
        (900, "CM"),
        (500, "D"),
        (400, "CD"),
        (100, "C"),
        (90, "XC"),
        (50, "L"),
        (40, "XL"),
        (10, "X"),
        (9, "IX"),
        (5, "V"),
        (4, "IV"),
        (1, "I"),
    ]
    roman = ""
    for value, letter in roman_numerals:
        while num >= value:
            roman += letter
            num -= value
    return roman
