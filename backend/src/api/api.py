"""
This module provides an API for interacting with musical instruments and their finger positions.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from src.instruments.neck_instrument import (
    Banjo,
    Bass,
    Guitar,
    Guitarlele,
    Mandolin,
    NeckInstrument,
    Ukulele,
)
from src.positions.neck_position import NeckPosition
from src.utils.note2num import note2num

from .get_all_pos_from_notes import get_all_pos_from_notes
from .get_best_pos_from_notes import get_best_pos_from_notes

INSTRUMENT_CLASSES: dict[str, type[NeckInstrument]] = {
    "Guitar": Guitar,
    "Ukulele": Ukulele,
    "Banjo": Banjo,
    "Mandolin": Mandolin,
    "Bass": Bass,
    "Guitarlele": Guitarlele,
}


class NoteInput(BaseModel):
    """This class represents the input for the getBestPosFromNotes API endpoint."""

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
def read_root() -> dict:
    """Root endpoint for the API."""
    return {"message": "Welcome to the Musical Instrument API!"}


@app.get("/getInstrumentDetails")
def get_instrument_details(instrument_name: str) -> dict:
    """
    Args:
        instrument (str): The instrument name

    Returns:
        dict: instrument details
    """
    instrument = NeckInstrument()
    if instrument_name in INSTRUMENT_CLASSES:
        instrument = INSTRUMENT_CLASSES[instrument_name]()
    else:
        return {"error": "Instrument not found."}
    return instrument.detail()


@app.post("/getBestPosFromNotes")
def get_best_pos_from_notes_api(note_input: NoteInput) -> dict:
    """
    This function takes a list of notes and an instrument and returns a position.

    Parameters:
        notes (List[str]): A list of notes.
        instrument (str): The name of the instrument.

    Returns:
        NPosition: The position to play the notes on the instrument.
    """

    if note_input.instrument in INSTRUMENT_CLASSES:
        instrument = INSTRUMENT_CLASSES[note_input.instrument]()
    else:
        return {"error": "Instrument not found."}

    notes_int = [note2num(note) for note in note_input.notes]

    position = get_best_pos_from_notes(notes_int, instrument)
    if not isinstance(position, NeckPosition):
        return {"error": "No valid position found for the given notes."}
    return position.to_json()


@app.post("/getAllPosFromNotes")
def get_all_pos_from_notes_api(note_input: NoteInput) -> dict:
    """
    This function takes a list of notes and an instrument and returns all positions.

    Parameters:
        notes (List[str]): A list of notes.
        instrument (str): The name of the instrument.

    Returns:
        dict: A dictionary mapping positions to their costs, or -1 if no valid positions are found.
    """

    if note_input.instrument in INSTRUMENT_CLASSES:
        instrument = INSTRUMENT_CLASSES[note_input.instrument]()
    else:
        return {"error": "Instrument not found."}

    notes_int = [note2num(note) for note in note_input.notes]

    positions_costs = get_all_pos_from_notes(notes_int, instrument)
    if isinstance(positions_costs, int):
        return {"error": "No valid positions found for the given notes."}

    return {num: (pos.to_json(), cost) for num, (pos, cost) in enumerate(positions_costs.items())}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)
