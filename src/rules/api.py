__author__ = "Eliot Christon"
__email__  = "eliot.christon@gmail.com"
__github__ = "eliot-christon"

from pydantic import BaseModel
from typing import List
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .getPosFromNotes import getPosFromNotes

class NoteInput(BaseModel):
    notes: List[str]
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
        instrument = Guitar()
    elif input.instrument == "Ukulele":
        from ..model.instrument.INeck import Ukulele
        instrument = Ukulele()
    elif input.instrument == "Banjo":
        from ..model.instrument.INeck import Banjo
        instrument = Banjo()
    elif input.instrument == "Mandolin":
        from ..model.instrument.INeck import Mandolin
        instrument = Mandolin()
    elif input.instrument == "Bass":
        from ..model.instrument.INeck import Bass
        instrument = Bass()
    else:
        return {"error": "Instrument not found."}
    
    from ..model.utils.note2num import note2num
    
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