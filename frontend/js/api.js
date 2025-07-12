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
