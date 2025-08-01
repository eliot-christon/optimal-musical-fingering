"""
Main script to run the api server for the optimal musical fingering application.

It also opens the frontend in a web browser.
"""

import sys
import webbrowser
from pathlib import Path

import uvicorn
from fastapi.staticfiles import StaticFiles

from backend.src.api.api import app

frontend_dir = Path(__file__).parent / "frontend"
app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="static")
if "--quiet" not in sys.argv:
    webbrowser.open("http://localhost:8000")
uvicorn.run(app, host="localhost", port=8000)
