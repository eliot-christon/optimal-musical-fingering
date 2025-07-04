/*
Author: Eliot Christon
email:  eliot.christon@gmail.com
github: eliot-christon
*/

// Main JavaScript file for the UI
// This file handles the dynamic generation of the instrument neck and API interactions


const instrumentSelect = document.getElementById('instrument');
const neckContainer = document.getElementById('neckContainer');
const fretboard = document.createElement('div');
const apiUrl = "http://localhost:8000";

// Function to create the neck based on selected instrument
function drawNeck(stringsCount, fretsCount, openStrings = []) {
    neckContainer.innerHTML = ''; // Clear existing neck

    const fretboard = document.createElement('div');
    fretboard.classList.add('fretboard');

    fretboard.style.setProperty('--strings-count', stringsCount);
    fretboard.style.setProperty('--frets-count', fretsCount + 1); // +1 to leave room for labels

    // Add open string labels (before nut)
    for (let string = 0; string < stringsCount; string++) {
        const stringLabel = document.createElement('div');
        stringLabel.classList.add('string-label');
        stringLabel.textContent = openStrings[string] || ''; // Use empty if undefined
        stringLabel.style.gridRow = `${string + 1}`;
        stringLabel.style.gridColumn = `1`; // Before nut

        fretboard.appendChild(stringLabel);
    }

    // Add nut line (first fret)
    const nutLine = document.createElement('div');
    nutLine.classList.add('nut');
    nutLine.style.gridRow = `1 / span ${stringsCount}`;
    nutLine.style.gridColumn = `2`; // After label column
    fretboard.appendChild(nutLine);

    // Create fret lines
    for (let fret = 0; fret < fretsCount; fret++) {
        const fretLine = document.createElement('div');
        fretLine.classList.add('fret');
        fretLine.style.gridRow = `1 / span ${stringsCount}`;
        fretLine.style.gridColumn = `${fret + 2}`; // +2 for label and nut
        if ([2, 4, 6, 8, 11, 14, 16, 18, 20, 23].includes(fret)) {
            const marker = document.createElement('div');
            marker.classList.add('fret-dot');
            marker.style.gridRow = `5 / span 1`;
            marker.style.gridColumn = `${fret + 2}`;
            fretLine.appendChild(marker);
        }
        fretboard.appendChild(fretLine);
    }

    // Create strings
    for (let string = 0; string < stringsCount; string++) {
        const stringLine = document.createElement('div');
        stringLine.classList.add('string');
        stringLine.style.gridRow = `${string + 1}`;
        stringLine.style.gridColumn = `2 / span ${fretsCount}`;
        fretboard.appendChild(stringLine);
    }

    neckContainer.appendChild(fretboard);
}

function drawPosition(data) {
    // Search for active fretboard
    const fretboard = document.querySelector('.fretboard');
    if (!fretboard || !data?.frets || !data?.strings) return;

    // Delete old markers
    fretboard.querySelectorAll('.note-position').forEach(marker => marker.remove());

    const { frets, strings, fingers } = data;

    for (let i = 0; i < frets.length; i++) {
        const fret = frets[i];
        const string = strings[i];
        const finger = fingers[i];

        const noteMarker = document.createElement('div');
        noteMarker.classList.add('note-position');
        noteMarker.textContent = finger === 0 ? 'O' : finger; // "O" pour corde à vide

        noteMarker.style.gridRow = `${string}`;
        noteMarker.style.gridColumn = `${fret + 1}`;

        fretboard.appendChild(noteMarker);
    }
}


// Event listener for instrument change to adjust neck visualization
instrumentSelect.addEventListener('change', function() {
    const selectedInstrument = instrumentSelect.value;

    fetch(`${apiUrl}/getInstrumentDetails?instrument_name=${selectedInstrument}`)
    .then(response => {
        if (!response.ok) {
            throw new Error(`Failed to fetch instrument details: ${response.statusText}`);
        }
        return response.json();
    })
    .then(data => {
        const frets = data.frets || 12;
        const openStrings = data.strings || ["E4"];
        drawNeck(openStrings.length, frets, openStrings);
    })
    .catch(error => {
        console.error('Error fetching instrument details:', error);
    });

});

// Handle submit button click
document.getElementById('submit').addEventListener('click', async function() {
    const notes = document.getElementById('notes').value;
    const selectedInstrument = instrumentSelect.value;
    // alert(`Notes: ${notes}, Instrument: ${selectedInstrument}`);

    // create notes array from input
    const notesArray = notes.split(' ').map(note => note.trim()).filter(note => note !== '');

    try {
        const response = await fetch(apiUrl + "/getPosFromNotes", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                notes: notesArray,
                instrument: selectedInstrument
            })
        });

        if (!response.ok) {
            throw new Error('Network response was not ok, status: ' + response.statusText);
        }

        const data = await response.json();
        console.log(data);

        drawPosition(data)


    } catch (error) {
        console.error('Error:', error);
    }
});