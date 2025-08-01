"""This file contains the pytest fixture to run the server before tests.
It ensures that the server is running before executing any tests that require it.
"""

import subprocess
import sys
import time
from collections.abc import Generator
from typing import Any

import pytest


@pytest.fixture(scope="session", autouse=True)
def run_server() -> Generator[Any, None, None]:
    """Fixture to run the server before tests."""
    with subprocess.Popen([sys.executable, "main.py", "--quiet"]) as proc:
        time.sleep(2)
        yield
        proc.terminate()
        proc.wait()
