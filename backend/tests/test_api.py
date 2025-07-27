"""
This is the test suite for the API endpoints of the musical instrument fingering application.
It tests the functionality of the endpoints that retrieve finger positions from musical notes.
"""

import pytest
import requests

URL = "http://localhost:8000"

# Ensure the server is running before executing these tests
pytestmark = pytest.mark.skip("Skipping tests that require a running server")


def test_get_best_pos_from_notes() -> None:
    """Test the retrieval of the best position from musical notes."""
    response = requests.post(
        f"{URL}/getBestPosFromNotes",
        json={
            "notes": ["C4", "E4", "G4"],
            "instrument": "Guitar",
        },
        headers={"Content-Type": "application/json"},
        timeout=10,
    )
    response = response.json()
    assert "strings" in response
    assert "frets" in response
    assert "fingers" in response
    assert len(response["strings"]) == len(response["frets"])
    assert len(response["strings"]) == len(response["fingers"])


def test_get_instrument_details() -> None:
    """Test the retrieval of instrument details."""
    response = requests.get(
        f"{URL}/getInstrumentDetails",
        params={
            "instrument_name": "Guitar",
        },
        headers={"Content-Type": "application/json"},
        timeout=10,
    )
    response = response.json()
    assert "strings" in response
    assert "frets" in response
    assert "range" in response
    assert "description" in response
    assert response["range"][0] < response["range"][1]
    assert isinstance(response["description"], str)
    assert isinstance(response["frets"], int)
