export function drawPosition(data) {
  const fretboard = document.querySelector('.fretboard')
  if (!fretboard || !data?.frets) return

  fretboard.querySelectorAll('.note-position').forEach(el => el.remove())

  data.frets.forEach((fret, i) => {
    const string = data.strings[i]
    const finger = data.fingers[i]

    const marker = document.createElement('div')
    marker.classList.add('note-position')
    marker.textContent = finger === 0 ? 'O' : finger
    marker.style.gridRow = string
    marker.style.gridColumn = fret + 1
    fretboard.appendChild(marker)
  })
}
