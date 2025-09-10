// Handles instrument selection and neck drawing
export function setupInstrumentSelect(
  instrumentSelect1,
  neckContainer,
  positionDifficulty,
  changePositionButton,
  difficultyValue
) {
  instrumentSelect1.addEventListener('change', async () => {
    const instrument1 = instrumentSelect1.value
    try {
      const { getInstrumentDetails } = await import('../api.js')
      const { drawNeck } = await import('./drawNeck.js')
      const data = await getInstrumentDetails(instrument1)
      drawNeck(neckContainer, data.strings.length, data.frets, data.strings)
      positionDifficulty.style.display = 'none'
      changePositionButton.style.display = 'none'
      difficultyValue.textContent = '0'
    } catch (error) {
      console.error('Loading instrument details failed:', error)
    }
  })
}
