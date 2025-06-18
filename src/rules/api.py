__author__ = "Eliot Christon"
__email__  = "eliot.christon@gmail.com"
__github__ = "eliot-christon"

from pydantic import BaseModel
from typing import List
from fastapi import FastAPI

from .getPosFromNotes import getPosFromNotes

class NoteInput(BaseModel):
    notes: List[str]
    instrument: str

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/getPosFromNotes")
def getPosFromNotesAPI(input: NoteInput):
    """
    This function takes a list of notes and an instrument and returns a position.

    Parameters:
        notes (List[str]): A list of notes.
        instrument (str): The name of the instrument.

    Returns:
        NPosition: The position to play the notes on the instrument.
    """
    
    if input.instrument == "Guitar":
        from ..model.instrument.INeck import Guitar
        from ..model.utils.note2num import note2num
        instrument = Guitar()
    else:
        return {"error": "Instrument not found."}
    
    notesInt = [note2num(note) for note in input.notes]

    return getPosFromNotes(notesInt, instrument).to_json()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)
    
    # simulating a post request
    import requests
    response = requests.post("http://localhost:8000/getPosFromNotes", json={
        "notes": ["C4", "E4", "G4"],
        "instrument": "Guitar",
    }, headers={"Content-Type": "application/json"})
    
    print(response.json())