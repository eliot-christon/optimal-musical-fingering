export function clearAllMOF() {
  uploadStatus.textContent = ''
  window.uploadedFileName = null // Clear the uploaded file name
  const fileInput = document.getElementById('fileInput')
  fileInput.value = '' // Clear the file input
  const optimalPositionsText = document.getElementById('optimalPositions')
  optimalPositionsText.value = '' // Clear the optimal positions text area
}
