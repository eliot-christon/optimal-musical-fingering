// Handles getting optimal positions from uploaded MIDI file
export function setupOptimalPositions(getOptimalPositionsButton, optimalPositionsText, instrumentSelect2) {
  getOptimalPositionsButton.addEventListener('click', async () => {
    optimalPositionsText.value = ''
    if (!window.uploadedFileName) {
      console.warn('No uploaded MIDI file found.')
      return
    }
    try {
      const { getOptimalPositionsFromMIDIFile } = await import('../api.js')
      const instrument2 = instrumentSelect2.value
      const data = await getOptimalPositionsFromMIDIFile(window.uploadedFileName, instrument2)
      for (const [num, pos] of Object.entries(data)) {
        const posStr =
          `Position ${num}: ` +
          pos.strings.map((s, i) => `String ${s}, Fret ${pos.frets[i]}, Finger ${pos.fingers[i]}`).join(' | ')
        optimalPositionsText.value += posStr + '\n'
      }
    } catch (error) {
      console.error('Loading optimal positions failed:', error)
      alert('Failed to get optimal positions. Please try again.')
    }
  })
}
