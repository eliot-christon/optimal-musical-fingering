/*
Author: Eliot Christon
email:  eliot.christon@gmail.com
github: eliot-christon
*/

// Main JavaScript file for the UI
// This file handles the dynamic generation of the instrument neck and API interactions


const instrumentSelect = document.getElementById('instrument');
const neckContainer = document.getElementById('neckContainer');

// Function to create the neck based on selected instrument
function drawNeck(stringsCount, fretsCount) {
    neckContainer.innerHTML = ''; // Clear existing neck

    // Create a container for the fretboard
    const fretboard = document.createElement('div');
    fretboard.classList.add('fretboard');

    fretboard.style.setProperty('--strings-count', stringsCount);
    fretboard.style.setProperty('--frets-count', fretsCount);

    // Create grid frets * strings
    for (let fret = 0; fret <= fretsCount; fret++) {
        const fretLine = document.createElement('div');
        fretLine.classList.add('fret');
        fretLine.style.gridRow = `1 / span ${stringsCount}`;
        fretLine.style.gridColumn = `${fret + 1}`;
        // add marker if fret is 3, 5, 7, 9, or 12 in the middle of the fret
        if ([2, 4, 6, 8, 11].includes(fret)) {
            const marker = document.createElement('div');
            marker.classList.add('fret-dot');
            marker.style.gridRow = `5 / span 1`; // Center the marker vertically
            marker.style.gridColumn = `${fret + 1}`;
            fretLine.appendChild(marker);
        }

        fretboard.appendChild(fretLine);
    }

    // Create strings
    for (let string = 0; string < stringsCount; string++) {
        const stringLine = document.createElement('div');
        stringLine.classList.add('string');
        stringLine.style.gridRow = `${string + 1}`;
        stringLine.style.gridColumn = `1 / span ${fretsCount + 1}`;
        fretboard.appendChild(stringLine);
    }

    // Append the fretboard to the neck container
    neckContainer.appendChild(fretboard);
}

// Event listener for instrument change to adjust neck visualization
instrumentSelect.addEventListener('change', function() {
    const selectedInstrument = instrumentSelect.value;
    if (selectedInstrument === 'Guitar') {
        drawNeck(6, 12); // Guitar with 6 strings
    } else if (selectedInstrument === 'Bass') {
        drawNeck(4, 12); // Bass with 4 strings
    } else if (selectedInstrument === 'Ukulele') {
        drawNeck(4, 10); // Ukulele with 4 strings
    }
});

// Draw the default neck on page load
drawNeck(6, 12); // Guitar is default

// Handle submit button click
// API call : post at url: "http://localhost:8000/getPosFromNotes"
const apiUrl = "http://localhost:8000/getPosFromNotes";
document.getElementById('submit').addEventListener('click', async function() {
    const notes = document.getElementById('notes').value;
    const selectedInstrument = instrumentSelect.value;
    // alert(`Notes: ${notes}, Instrument: ${selectedInstrument}`);

    // create notes array from input
    const notesArray = notes.split(' ').map(note => note.trim()).filter(note => note !== '');

    try {
        const response = await fetch(apiUrl, {
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

    } catch (error) {
        console.error('Error:', error);
    }
});