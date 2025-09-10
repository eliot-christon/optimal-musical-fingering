// Handles note submission, position sorting, changing positions, and difficulty display
export function setupPositionHandlers(
  submitButton,
  notesInput,
  instrumentSelect1,
  positionDifficulty,
  changePositionButton,
  difficultyValue
) {
  submitButton.addEventListener('click', async () => {
    const notes = notesInput.value.trim().split(' ').filter(Boolean)
    const instrument1 = instrumentSelect1.value
    try {
      const { getAllPosFromNotes } = await import('../api.js')
      const { drawPosition } = await import('./drawPosition.js')
      const data = await getAllPosFromNotes(notes, instrument1)
      if ('error' in data) {
        alert(`${data.error}`)
        window.positions = []
        window.currentPositionIndex = 0
        return
      }
      const sortedPositions = Object.entries(data).sort((a, b) => a[1][1] - b[1][1])
      window.positions = sortedPositions
      window.currentPositionIndex = 0
      const difficulty = sortedPositions[0][1][1]
      difficultyValue.textContent = difficulty
      positionDifficulty.style.display = 'block'
      changePositionButton.style.display = 'block'
      drawPosition(sortedPositions[0][1][0])
    } catch (error) {
      console.error('Loading API call failed:', error)
    }
  })

  changePositionButton.addEventListener('click', async () => {
    if (!window.positions || window.positions.length === 0) {
      return
    }
    window.currentPositionIndex = (window.currentPositionIndex + 1) % window.positions.length
    const currentPosition = window.positions[window.currentPositionIndex][1][0]
    const { drawPosition } = await import('./drawPosition.js')
    drawPosition(currentPosition)
    const difficulty = window.positions[window.currentPositionIndex][1][1]
    difficultyValue.textContent = Math.round(difficulty)
  })
}
