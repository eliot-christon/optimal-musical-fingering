import { CONFIG } from '../env.js'

export async function getInstrumentDetails(instrumentName) {
  const res = await fetch(`${CONFIG.API_URL}/getInstrumentDetails?instrument_name=${instrumentName}`)
  if (!res.ok) throw new Error('API call failed')
  return res.json()
}

export async function getBestPosFromNotes(notes, instrument) {
  const res = await fetch(`${CONFIG.API_URL}/getBestPosFromNotes`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ notes, instrument }),
  })
  if (!res.ok) throw new Error('API call failed')
  return res.json()
}

export async function getAllPosFromNotes(notes, instrument) {
  const res = await fetch(`${CONFIG.API_URL}/getAllPosFromNotes`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ notes, instrument }),
  })
  if (!res.ok) throw new Error('API call failed')
  return res.json()
}

export async function uploadMIDIFile(file) {
  const formData = new FormData()
  formData.append('file', file)

  const res = await fetch(`${CONFIG.API_URL}/upload`, {
    method: 'POST',
    body: formData,
  })
  if (!res.ok) throw new Error('File upload failed')
  return res.json()
}

export async function getOptimalPositionsFromMIDIFile(midiFileName, instrumentName) {
  const res = await fetch(`${CONFIG.API_URL}/midi2optimalPositions`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ midi_file_name: midiFileName, instrument_name: instrumentName }),
  })
  if (!res.ok) throw new Error('API call failed')
  return res.json()
}
