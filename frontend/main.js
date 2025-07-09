import { getInstrumentDetails, getBestPosFromNotes } from './js/api.js'
import { drawNeck } from './js/drawNeck.js'
import { drawPosition } from './js/drawPosition.js'

const instrumentSelect = document.getElementById('instrument')
const neckContainer = document.getElementById('neckContainer')
const submitButton = document.getElementById('submit')
const notesInput = document.getElementById('notes')

// ⚡️ Au changement d'instrument
instrumentSelect.addEventListener('change', async () => {
  const instrument = instrumentSelect.value
  try {
    const data = await getInstrumentDetails(instrument)
    drawNeck(neckContainer, data.strings.length, data.frets, data.strings)
  } catch (error) {
    console.error("Erreur lors du chargement de l'instrument:", error)
  }
})

// ⚡️ Soumission des notes
submitButton.addEventListener('click', async () => {
  const notes = notesInput.value.trim().split(' ').filter(Boolean)
  const instrument = instrumentSelect.value
  try {
    const data = await getBestPosFromNotes(notes, instrument)
    drawPosition(data)
  } catch (error) {
    console.error("Erreur lors de l'appel API:", error)
  }
})
