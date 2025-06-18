__author__ = "Eliot Christon"
__email__  = "eliot.christon@gmail.com"
__github__ = "eliot-christon"

from typing import List
from fastapi import FastAPI

from .getPosFromNotes import getPosFromNotes

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/getPosFromNotes")
def getPosFromNotesAPI(notes: List[str], instrument: str):
    """
    This function takes a list of notes and an instrument and returns a position.

    Parameters:
        notes (List[str]): A list of notes.
        instrument (str): The name of the instrument.

    Returns:
        NPosition: The position to play the notes on the instrument.
    """
    
    if instrument == "Guitar":
        from ..model.instrument.INeck import Guitar
        from ..model.utils.note2num import note2num
        instrument = Guitar()
    else:
        return {"error": "Instrument not found."}
    
    notesInt = [note2num(note) for note in notes]

    return getPosFromNotes(notesInt, instrument).to_json()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)