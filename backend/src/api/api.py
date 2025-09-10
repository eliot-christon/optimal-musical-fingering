"""
This module provides an API for interacting with musical instruments and their finger positions.
"""

from pathlib import Path
from typing import Annotated

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from backend.src.instruments.neck_instrument import (
    Banjo,
    Bass,
    Guitar,
    Guitarlele,
    Mandolin,
    NeckInstrument,
    Ukulele,
)
from backend.src.positions.neck_position import NeckPosition
from backend.src.utils.note2num import note2num

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


ALLOWED_EXTENSIONS = {".mid"}
MIDI_FILE_UPLOAD_FOLDER = Path(__file__).parents[3] / ".uploads" / "midi"
MIDI_FILE_UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)


def allowed_file(filename: str) -> bool:
    """Check if the file has an allowed extension."""
    return any(filename.endswith(ext) for ext in ALLOWED_EXTENSIONS)


@app.post("/upload/")
async def upload_file(file: Annotated[UploadFile, File()]) -> dict:
    """Upload a MIDI file to the server."""
    if not file.filename:
        raise HTTPException(status_code=400, detail="No filename provided")
    if not allowed_file(file.filename):
        raise HTTPException(status_code=400, detail="Invalid file extension")
    with Path.open(MIDI_FILE_UPLOAD_FOLDER / file.filename, "wb", encoding="utf-8") as f:
        f.write(await file.read())
    return {"info": f"file '{file.filename}' saved"}


@app.get("/", response_class=HTMLResponse)
def read_root() -> HTMLResponse:
    """Root endpoint for the API, returns the frontend HTML."""
    index_path = Path(__file__).parents[3] / "frontend" / "index.html"
    if index_path.exists():
        return HTMLResponse(content=index_path.read_text(encoding="utf-8"))
    return HTMLResponse(content="<h1>index.html not found</h1>")


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
