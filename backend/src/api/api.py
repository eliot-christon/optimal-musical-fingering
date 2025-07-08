"""
This module provides an API for interacting with musical instruments and their finger positions.
"""

__author__ = "Eliot Christon"
__email__ = "eliot.christon@gmail.com"
__github__ = "eliot-christon"


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from ..instruments.neck_instrument import (
    Banjo,
    Bass,
    Guitar,
    Guitarlele,
    Mandolin,
    NeckInstrument,
    Ukulele,
)
from ..utils.note2num import note2num
from .get_pos_from_notes import get_pos_from_notes

instrument_classes = {
    "Guitar": Guitar,
    "Ukulele": Ukulele,
    "Banjo": Banjo,
    "Mandolin": Mandolin,
    "Bass": Bass,
    "Guitarlele": Guitarlele,
}


class NoteInput(BaseModel):
    """This class represents the input for the getPosFromNotes API endpoint."""

    notes: list[str]
    instrument: str


app = FastAPI()

# Allow CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


@app.get("/")
def read_root():
    """Root endpoint for the API."""
    return {"message": "Welcome to the Musical Instrument API!"}


@app.get("/getInstrumentDetails")
def get_instrument_details(instrument_name: str):
    """
    Args:
        instrument (str): The instrument name

    Returns:
        dict: instrument details
    """
    instrument = NeckInstrument()
    if instrument_name in instrument_classes:
        instrument = instrument_classes[instrument_name]()
    else:
        return {"error": "Instrument not found."}
    return instrument.detail()


@app.post("/getPosFromNotes")
def get_pos_from_notes_api(note_input: NoteInput):
    """
    This function takes a list of notes and an instrument and returns a position.

    Parameters:
        notes (List[str]): A list of notes.
        instrument (str): The name of the instrument.

    Returns:
        NPosition: The position to play the notes on the instrument.
    """

    if note_input.instrument in instrument_classes:
        instrument = instrument_classes[note_input.instrument]()
    else:
        return {"error": "Instrument not found."}

    notes_int = [note2num(note) for note in note_input.notes]

    return get_pos_from_notes(notes_int, instrument).to_json()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)
