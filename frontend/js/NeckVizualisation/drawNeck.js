export function drawNeck(container, stringsCount, fretsCount, openStrings = []) {
  container.innerHTML = ''
  const fretboard = document.createElement('div')
  fretboard.classList.add('fretboard')
  fretboard.style.setProperty('--strings-count', stringsCount)
  fretboard.style.setProperty('--frets-count', fretsCount + 1)

  // Labels
  openStrings.forEach((label, i) => {
    const el = document.createElement('div')
    el.classList.add('string-label')
    el.textContent = label
    el.style.gridRow = i + 1
    el.style.gridColumn = 1
    fretboard.appendChild(el)
  })

  // Nut
  const nut = document.createElement('div')
  nut.classList.add('nut')
  nut.style.gridRow = `1 / span ${stringsCount}`
  nut.style.gridColumn = 2
  fretboard.appendChild(nut)

  // Frets
  for (let f = 0; f < fretsCount; f++) {
    const fret = document.createElement('div')
    fret.classList.add('fret')
    fret.style.gridRow = `1 / span ${stringsCount}`
    fret.style.gridColumn = f + 2
    if ([2, 4, 6, 8, 11, 14, 16, 18, 20, 23].includes(f)) {
      const dot = document.createElement('div')
      dot.classList.add('fret-dot')
      dot.style.gridRow = `5`
      dot.style.gridColumn = f + 2
      fret.appendChild(dot)
    }
    fretboard.appendChild(fret)
  }

  // Strings
  for (let s = 0; s < stringsCount; s++) {
    const string = document.createElement('div')
    string.classList.add('string')
    string.style.gridRow = s + 1
    string.style.gridColumn = `2 / span ${fretsCount}`
    fretboard.appendChild(string)
  }

  container.appendChild(fretboard)
}
