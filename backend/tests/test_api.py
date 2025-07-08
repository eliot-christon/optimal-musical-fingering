"""
This is the test suite for the API endpoints of the musical instrument fingering application.
It tests the functionality of the endpoints that retrieve finger positions from musical notes.
"""

__author__ = "Eliot Christon"
__email__ = "eliot.christon@gmail.com"
__github__ = "eliot-christon"

import unittest

import requests

URL = "http://localhost:8000"


class TestAPI(unittest.TestCase):
    """Test suite for the API endpoints of the musical instrument fingering application.

    Args:
        unittest (module): The unittest module.
    """

    def test_get_pos_from_notes(self) -> None:
        """Test the /getPosFromNotes endpoint with a set of notes and an instrument."""
        response = requests.post(
            f"{URL}/getPosFromNotes",
            json={
                "notes": ["C4", "E4", "G4"],
                "instrument": "Guitar",
            },
            headers={"Content-Type": "application/json"},
            timeout=10,
        )
        response = response.json()
        self.assertIn("strings", response)
        self.assertIn("frets", response)
        self.assertIn("fingers", response)
        self.assertEqual(len(response["strings"]), len(response["frets"]))
        self.assertEqual(len(response["strings"]), len(response["fingers"]))

    def test_get_instrument_details(self) -> None:
        """Test the /getInstrumentDetails endpoint with a specific instrument."""
        response = requests.get(
            f"{URL}/getInstrumentDetails",
            params={
                "instrument_name": "Guitar",
            },
            headers={"Content-Type": "application/json"},
            timeout=10,
        )
        response = response.json()
        self.assertIn("strings", response)
        self.assertIn("frets", response)
        self.assertIn("range", response)
        self.assertIn("description", response)
        self.assertLess(response["range"][0], response["range"][1])
        self.assertTrue(isinstance(response["description"], str))
        self.assertTrue(isinstance(response["frets"], int))


if __name__ == "__main__":
    unittest.main()
