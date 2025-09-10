// Minimal main.js: imports and initializes modules
import { setupInstrumentSelect } from './js/NeckVizualisation/instrumentHandler.js'
import { setupPositionHandlers } from './js/NeckVizualisation/positionHandler.js'
import { setupMidiUpload } from './js/MidiOptimalFingering/uploadHandler.js'
import { setupOptimalPositions } from './js/MidiOptimalFingering/optimalPositionHandler.js'
import { setupNightMode } from './js/theme.js'
import { clearAll } from './js/clearAll.js'

// DOM elements
const instrumentSelect1 = document.getElementById('instrument1')
const instrumentSelect2 = document.getElementById('instrument2')
const neckContainer = document.getElementById('neckContainer')
const submitButton = document.getElementById('submit')
const notesInput = document.getElementById('notes')
const changePositionButton = document.getElementById('changePosition')
const positionDifficulty = document.getElementById('positionDifficulty')
const difficultyValue = document.getElementById('difficultyValue')
const midiUploadForm = document.getElementById('uploadForm')
const uploadStatus = document.getElementById('uploadStatus')
const optimalPositionsText = document.getElementById('optimalPositions')
const getOptimalPositionsButton = document.getElementById('getOptimalPositions')
const nightModeToggle = document.getElementById('nightModeToggle')

// Clear all
clearAll()

// Initialize modules
setupInstrumentSelect(instrumentSelect1, neckContainer, positionDifficulty, changePositionButton, difficultyValue)
setupPositionHandlers(
  submitButton,
  notesInput,
  instrumentSelect1,
  positionDifficulty,
  changePositionButton,
  difficultyValue
)
setupMidiUpload(midiUploadForm, uploadStatus)
setupOptimalPositions(getOptimalPositionsButton, optimalPositionsText, instrumentSelect2)
setupNightMode(nightModeToggle)
