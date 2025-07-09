import { CONFIG } from '../env.js'

export async function getInstrumentDetails(instrumentName) {
  const res = await fetch(`${CONFIG.API_URL}/getInstrumentDetails?instrument_name=${instrumentName}`)
  if (!res.ok) throw new Error('Erreur API instrument')
  return res.json()
}

export async function getBestPosFromNotes(notes, instrument) {
  const res = await fetch(`${CONFIG.API_URL}/getBestPosFromNotes`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ notes, instrument }),
  })
  if (!res.ok) throw new Error('Erreur API position')
  return res.json()
}
