__author__ = "Eliot Christon"
__email__  = "eliot.christon@gmail.com"
__github__ = "eliot-christon"

import unittest
import requests


URL = "http://localhost:8000"


class TestAPI(unittest.TestCase):
    def test_getPosFromNotes(self):
        response = requests.post(f"{URL}/getPosFromNotes", json={
            "notes": ["C4", "E4", "G4"],
            "instrument": "Guitar",
        }, headers={"Content-Type": "application/json"})
        response = response.json()
        self.assertIn("strings", response)
        self.assertIn("frets", response)
        self.assertIn("fingers", response)
        self.assertEqual(len(response["strings"]), len(response["frets"]))
        self.assertEqual(len(response["strings"]),len(response["fingers"]))
    
    def test_getInstrumentDetails(self):
        response = requests.get(f"{URL}/getInstrumentDetails", json={
            "instrument": "Guitar",
        }, headers={"Content-Type": "application/json"})
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