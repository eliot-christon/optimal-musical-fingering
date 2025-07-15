export function clearAll() {
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
  const instrumentSelect = document.getElementById('instrument')
  instrumentSelect.dispatchEvent(new Event('change')) // Trigger change event to reset neck
}
