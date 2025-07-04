__author__ = "Eliot Christon"
__email__  = "eliot.christon@gmail.com"
__github__ = "eliot-christon"

from pydantic import BaseModel
from typing import List
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .getPosFromNotes import getPosFromNotes
from ..model.instrument.INeck import Guitar, Ukulele, Bass, Banjo, Mandolin, INeck

instrument_classes = {
    "Guitar"  : Guitar,
    "Ukulele" : Ukulele,
    "Banjo"   : Banjo,
    "Mandolin": Mandolin,
    "Bass"    : Bass,
}

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

@app.get("/getInstrumentDetails")
def getInstrumentDetails(instrument_name: str):
    """
    Args:
        instrument (str): The instrument name

    Returns:
        dict: instrument details
    """
    instrument = INeck()
    if instrument_name in instrument_classes.keys():
        instrument = instrument_classes[instrument_name]()
    else:
        return {"error": "Instrument not found."}
    return instrument.detail()


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
    
    if input.instrument in instrument_classes.keys():
        instrument = instrument_classes[input.instrument]()
    else:
        return {"error": "Instrument not found."}
    
    from ..model.utils.note2num import note2num
    
    notesInt = [note2num(note) for note in input.notes]

    return getPosFromNotes(notesInt, instrument).to_json()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)