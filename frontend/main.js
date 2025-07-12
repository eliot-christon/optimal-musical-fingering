import { getInstrumentDetails, getBestPosFromNotes, getAllPosFromNotes } from './js/api.js'
import { drawNeck } from './js/drawNeck.js'
import { drawPosition } from './js/drawPosition.js'
import { clearAll } from './js/clearAll.js'

const instrumentSelect = document.getElementById('instrument')
const neckContainer = document.getElementById('neckContainer')
const submitButton = document.getElementById('submit')
const notesInput = document.getElementById('notes')
const changePositionButton = document.getElementById('changePosition')
const positionDifficulty = document.getElementById('positionDifficulty')
const difficultyValue = document.getElementById('difficultyValue')

// ⚡️ On instrument change
instrumentSelect.addEventListener('change', async () => {
  const instrument = instrumentSelect.value
  try {
    const data = await getInstrumentDetails(instrument)
    drawNeck(neckContainer, data.strings.length, data.frets, data.strings)
    // Hide the difficulty box initially
    positionDifficulty.style.display = 'none'
    difficultyValue.textContent = '0' // Reset difficulty value
  } catch (error) {
    console.error('Loading instrument details failed:', error)
  }
})

// ⚡️ On notes submission
submitButton.addEventListener('click', async () => {
  const notes = notesInput.value.trim().split(' ').filter(Boolean)
  const instrument = instrumentSelect.value
  try {
    const data = await getAllPosFromNotes(notes, instrument)
    // data is a dictionary as follows:
    // { "0": (position_json, cost), "1": (position_json, cost), ... }

    // if error then data is {"error": "msg" }
    if ('error' in data) {
      console.error('API call error:', data.error)
      alert(`${data.error}`)
      clearAll() // Clear the neck container and reset state
      return
    }

    // now sort the positions by cost
    const sortedPositions = Object.entries(data).sort((a, b) => a[1][1] - b[1][1])
    // store all positions in a global variable for later use
    window.positions = sortedPositions
    window.currentPositionIndex = 0
    // Update the difficulty value
    const difficulty = sortedPositions[0][1][1]
    difficultyValue.textContent = difficulty
    positionDifficulty.style.display = 'block' // Show the difficulty box
    // draw the first position
    drawPosition(sortedPositions[0][1][0])
    console.log('Positions data:', data)
  } catch (error) {
    console.error('Loading API call failed:', error)
  }
})

// Position change
changePositionButton.addEventListener('click', () => {
  if (!window.positions || window.positions.length === 0) {
    console.warn('No positions available to change.')
    return
  }
  // Increment the current position index
  window.currentPositionIndex = (window.currentPositionIndex + 1) % window.positions.length
  const currentPosition = window.positions[window.currentPositionIndex][1][0]
  // Draw the new position
  drawPosition(currentPosition)
  // Update the difficulty value
  const difficulty = window.positions[window.currentPositionIndex][1][1]
  difficultyValue.textContent = difficulty.toFixed(2)
})
