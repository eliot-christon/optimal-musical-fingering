// Handles MIDI file upload form and status
export function setupMidiUpload(midiUploadForm, uploadStatus) {
  midiUploadForm.addEventListener('submit', async event => {
    event.preventDefault()
    const fileInput = document.getElementById('fileInput')
    const file = fileInput.files[0]
    if (!file) {
      alert('Please select a MIDI file to upload.')
      return
    }
    try {
      const { uploadMIDIFile } = await import('../api.js')
      const response = await uploadMIDIFile(file)
      uploadStatus.textContent = response.info
      window.uploadedFileName = file.name
    } catch (error) {
      uploadStatus.textContent = 'File upload failed.'
      alert('MIDI file upload failed. Please try again.')
    }
  })
}
