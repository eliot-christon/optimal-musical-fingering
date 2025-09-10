export function clearAllNV() {
  window.positions = []
  window.currentPositionIndex = 0
  document.getElementById('notes').value = ''
  document.getElementById('difficultyValue').textContent = '0'
  document.getElementById('positionDifficulty').style.display = 'none'
  document.getElementById('changePosition').style.display = 'none'
  const neckContainer = document.getElementById('neckContainer')
  while (neckContainer.firstChild) {
    neckContainer.removeChild(neckContainer.firstChild)
  }
  const instrumentSelect1 = document.getElementById('instrument1')
  instrumentSelect1.dispatchEvent(new Event('change')) // Trigger change event to reset neck
}
